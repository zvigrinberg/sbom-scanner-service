import os
from pathlib import Path
import logging

import requests
from requests import RequestException

logger = logging.getLogger(__name__)


def download(product_id: str) -> bytes | None:
    """Download product sbom from SBOM base url, using supplied environment variables, And save it to Cache dir.
       If already in cache, then do not download and just read it from there.
       Returns the file content or None if download failed."""
    base_url = os.getenv("SBOM_BASE_URL", "https://security.access.redhat.com/data/sbom/beta/spdx/")
    sbom_file_suffix = os.getenv("SBOM_FILE_SUFFIX", ".z.json.bz2")
    sbom_file_suffix2 = os.getenv("SBOM_FILE_SUFFIX", ".json.bz2")
    product_name_version_delimiter_web = os.getenv("PROD_NAME_VERSION_DELIMITER_REMOTE", "-")
    product_name_version_delimiter_input = os.getenv("PROD_NAME_VERSION_DELIMITER_INPUT", ":")
    document_mime_type = os.getenv("SBOM_DOCUMENT_MIME_TYPE", "application/x-bzip2")
    file_name = product_id.replace(product_name_version_delimiter_input,
                                   product_name_version_delimiter_web) + sbom_file_suffix
    sbom_url = base_url + file_name
    download_cache_location = os.getenv("DOWNLOAD_CACHE_LOCATION", "/data/sbom")
    file_path = f'{download_cache_location}/{file_name}'
    if not os.path.exists(file_path):
        headers = {"Accept": document_mime_type,
                   'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,"
                                 " like Gecko) Chrome/128.0.0.0 Safari/537.36"}
        return download_action(file_path, headers, sbom_url, sbom_file_suffix, sbom_file_suffix2)
    else:
        return Path(file_path).read_bytes()


def download_action(file_path, headers, sbom_url,sbom_file_suffix, sbom_file_suffix2) -> bytes | None:
    """this function download the desired sbom specified in sbom_url, if it can't find it or another error happened, returns None,
    otherwise, save it to file and return the contents in byth"""
    try:
        request = requests.get(sbom_url, headers=headers)
        if request.status_code == 200:
            content = save_file(file_path, request)
        else:
            sbom_url_modified = sbom_url.replace(sbom_file_suffix, sbom_file_suffix2)
            request = requests.get(sbom_url_modified, headers=headers)
            if request.status_code == 200:
                content = save_file(file_path, request)
            else:
                return request.status_code, request.reason

    except RequestException as err:
        logger.info(f"Failed to download sbom from {sbom_url}, {err.response} "
                    f"code={err.response.status_code},{err.response.reason}")
        return None

    return content


def save_file(file_path, request):
    content = request.content
    Path(file_path).write_bytes(content)
    return content
