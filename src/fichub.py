import requests


def get_fic_data(url, format_type):
    response = requests.get(
        "https://fichub.net/api/v0/epub?q="+url, allow_redirects=True).json()

    if format_type == 0:
        cache_url = response['epub_url']
        file_format = ".epub"

    elif format_type == 1:
        cache_url = response['mobi_url']
        file_format = ".mobi"

    elif format_type == 2:
        cache_url = response['pdf_url']
        file_format = ".pdf"

    elif format_type == 3:
        cache_url = response['html_url']
        file_format = ".zip"

    fic_name = response['epub_url'].split("/")[4].split("?")[0]
    fic_name = fic_name.replace(".epub", "")
    download_url = "https://fichub.net"+cache_url
    data = requests.get(download_url, allow_redirects=True).content

    return fic_name + file_format, data
