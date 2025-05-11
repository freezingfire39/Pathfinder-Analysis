# how to transfer data to others host
1. run s3_uploader_all dag or run the command: 
python /home/app/Desktop/Pathfinder-Analysis/airflow_pipeline/s3_operator/compressAndUploader.py /home/app/Desktop/output_china,/home/app/Desktop/output_search,/home/app/Desktop/default_portfolio
2. in others host run the following command:
rm -r ~/Desktop/default_portfolio
./decompressAndDownloader --keys default_portfolio.zip --dir /home/app/Desktop
rm -r ~/Desktop/output_search
./decompressAndDownloader --keys output_search.zip --dir /home/app/Desktop
rm -r ~/Desktop/output_china
3. ./decompressAndDownloader --keys output_china.zip --dir /home/app/Desktop