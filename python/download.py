from ffiec_data_collector import FFIECDownloader, Product, FileFormat


REPORTING_PERIOD = "20241231"


def download_call_report():

    downloader = FFIECDownloader()

    result = downloader.download(
        product=Product.CALL_SINGLE,
        period=REPORTING_PERIOD,
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