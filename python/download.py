from ffiec_data_collector import FFIECDownloader, Product, FileFormat


def download_call_report():

    downloader = FFIECDownloader()

    result = downloader.download(
        product=Product.CALL_SINGLE,
        period="20240331",
        format=FileFormat.TSV
    )

    if result.success:
        print("Download successful!")
        print(f"File: {result.filename}")
        print(f"Location: {result.file_path}")
    else:
        print("Download failed.")
        print(result.error_message)


if __name__ == "__main__":
    download_call_report()
