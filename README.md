# Face Detection Docker
![img](https://github.com/vyzboy92/face-detection-docker/blob/master/templates/face.png)

A containarized face app that detects faces from a usb-camera and streams it to a browser.

The stream can be accessed at ```http://localhost:4000``` on the browser. It can be viewed with zero latency on multiple devices by connecting to same network as the main PC.

Make sure that docker and docker-compose are installed.

The project explores how processed image data can be visualized as a stream with the help of OpenCV from inside a docker without the gtk support.

## Run the app

To run the application on a PC running Ubuntu, connected to a usb camera, from a terminal run ```docker-compose up```.

This will connect to default camera at ```/dev/video0```.

If you have other cameras connected, then run ```v4l2-ctl --list-devices``` to list available devices and change the volume mount path inside ```docker-compose.yml```file.
