# How to use

In the k8s folder contains all the files to deploy the Yolo network. Two different versions of the Yolo network are available, namely stegala/yolo-server:tiny and stegala/yolo-server:reg to be specified as an image.

The client is in the src folder. Can be executed as 

```
python3 client.py
```

The main function is

```
process_image_repeatedly(20, 600, 'http://ip:port/process_frames')
```

which requires as argument the framerate (fps), the duration (in seconds) of the test, and the URL of the server (replace it the IP and the port of the server).

The script will the generate a 'result.dat' file containing information on the excpected framerate and the measured framerate computed as the average throughout the test. 

