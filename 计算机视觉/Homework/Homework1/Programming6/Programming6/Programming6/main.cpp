#include <iostream>
#include <string>
#include <opencv2/opencv.hpp>

using namespace std;

int main()
{

	cv::Mat imgl = cv::imread("l.jpg");
	cv::Mat imgr = cv::imread("r.jpg");
	if (!imgl.data || !imgr.data)
	{
		cout << "Reading Images Failure!" << endl;
		return -1;
	}
	auto orbDetector = cv::ORB::create();
	vector<cv::KeyPoint> kpsl, kpsr;
	cv::Mat dcpsl, dcpsr;

	orbDetector->detectAndCompute(imgl, cv::Mat(), kpsl, dcpsl);
	orbDetector->detectAndCompute(imgr, cv::Mat(), kpsr, dcpsr);

	cv::Ptr<cv::DescriptorMatcher> matcher = cv::DescriptorMatcher::create(cv::DescriptorMatcher::BRUTEFORCE);
	std::vector<cv::DMatch> matchers;
	matcher->match(dcpsl, dcpsr, matchers);

	cv::Mat imgMatches;
	drawMatches(imgl, kpsl, imgr, kpsr, matchers, imgMatches);

	imshow("Match", imgMatches);

	cv::waitKey(0);

	cv::imwrite("Match.jpg", imgMatches);

	return true;
}