#include "opencv2/opencv.hpp"

using namespace cv;

int main(int argc, char **argv)
{
	Mat img, gray;
	if(argc == 2)
		img = cv::imread(argv[1], 1);
	else
		img = cv::imread("img1.png", 1);

	for(int i = 0; i < 10000; i++){
		cv::cvtColor(img, gray, cv::COLOR_BGR2GRAY);
		cv::GaussianBlur(gray, gray, cv::Size(7, 7), 1.5);
		cv::Canny(gray, gray, 0, 50);
	}

	cv::imshow("original", img);
	cv::imshow("edges", gray);
	cv::waitKey(100);

	return 0;
}
