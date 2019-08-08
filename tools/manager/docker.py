import boto3
from subprocess import Popen

def fetch_image_from_s3(image):
    print("trying to download image %s" % image)
    s3 = boto3.client('s3')
    s3.download_file("halite2", image, image)

def load_in_docker(image):
    p = Popen(["./docker_load.sh", image])
    p.wait()
    return p

if __name__ == "__main__":
    image = "bots/hbot.tar.gz"
    # fetch_image_from_s3(image)
    load_in_docker(image)