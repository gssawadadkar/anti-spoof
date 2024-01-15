package listeners;

import java.io.IOException;

import org.openqa.selenium.WebDriver;
import org.testng.ITestListener;
import org.testng.ITestResult;

import com.aventstack.extentreports.ExtentTest;

import coverFoxBase.Base;
import coverFoxUtility.Utility;

public class ListenerCoverFox extends Base implements ITestListener
{
	ThreadLocal<ExtentTest> extentTest =new ThreadLocal<ExtentTest>();

	
	@Override
	public void onTestFailure(ITestResult result) 
	{
		
//extentTest.get().fail(result.getThrowable());
//		
//		String testmethodname=result.getMethod().getMethodName();
//		
//		try {
//			driver= (WebDriver)result.getTestClass().getRealClass().getDeclaredField("driver").get(result.getInstance());
//		} catch (Exception e) {
//			e.printStackTrace();	
//		}
//		
//		try {
//			extentTest.get().addScreenCaptureFromPath(Utility.takeScreenShot(driver, result.getName()),result.getMethod().getMethodName());
//		} catch (IOException e) {
//			e.printStackTrace();
//		}
//		
	}
	
	@Override
	public void onTestSuccess(ITestResult result) {
		
	}

	@Override
	public void onTestSkipped(ITestResult result) {
		
	}
}
