from package.wikipedia_scrap import Wikipedia
from package.package_minio import Minio

if __name__ == '__main__':
    url = 'https://en.wikipedia.org/wiki/List_of_association_football_stadiums_by_capacity'
    wiki = Wikipedia(url)
    data = wiki.get_data()
    # print(data)
    # upload data ke minio
    minio_instance = Minio()
    load_data = minio_instance.upload_data_minio(data)
    get_data = minio_instance.get_data_minio(load_data)
    print('selesai')