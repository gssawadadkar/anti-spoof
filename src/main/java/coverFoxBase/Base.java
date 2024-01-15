package coverFoxBase;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.testng.Reporter;

public class Base 
{
	static protected WebDriver driver;
	//open browser
	
	public void launchCoverFox() throws InterruptedException
	{
		driver= new ChromeDriver();
		driver.manage().window().maximize();
		Reporter.log("Launching browser ", true);
		driver.get("https://www.coverfox.com/");
		Thread.sleep(1000);
	}
	
	
	//close Browser
	
	public void closeCoverFox() throws InterruptedException
	{
		Reporter.log("Closing browser ", true);
		Thread.sleep(1000);
		driver.close();
	}

}
