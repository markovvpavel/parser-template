from tqdm import tqdm
import requests


def load_cookies(cookies_file):
    cookies = {}
    with open(cookies_file, 'r') as file:
        for line in file:
            if line.startswith('#'):
                continue
            fields = line.strip().split('\t')
            if len(fields) == 7:
                domain, flag, path, secure, expiration_time, name, value = fields
                cookies[name] = value
    return cookies


async def download_file(url, output_path, cookies_file=None, referer=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'video/mp4',
    }

    if referer:
        headers['Referer'] = referer

    cookies = {}

    if cookies_file:
        cookies = load_cookies(cookies_file)

    response = requests.get(url, stream=True, cookies=cookies, headers=headers)

    if response.status_code != 200:
        print(response)
        return False

    total_size = int(response.headers.get('content-length', 0))

    five_hundred_mb_in_bytes = 500 * 1024 * 1024

    if total_size >= five_hundred_mb_in_bytes:
        return False

    chunk_size = 8192

    with open(output_path, 'wb') as file:
        with tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024, desc="Downloading") as progress_bar:
            for chunk in response.iter_content(chunk_size=chunk_size):
                file.write(chunk)
                progress_bar.update(len(chunk))

    return True
