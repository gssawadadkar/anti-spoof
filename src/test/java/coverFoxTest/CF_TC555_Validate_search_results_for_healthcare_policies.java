package coverFoxTest;

import java.io.IOException;
import java.time.Duration;

import org.apache.log4j.Logger;
import org.apache.log4j.PropertyConfigurator;
import org.apache.poi.EncryptedDocumentException;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.testng.Assert;
import org.testng.Reporter;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Listeners;
import org.testng.annotations.Test;

import coverFoxBase.Base;
import coverFoxPOM.CoverFoxAddressDetailsPage;
import coverFoxPOM.CoverFoxHealthPlanPage;
import coverFoxPOM.CoverFoxHealthPlanResultsPage;
import coverFoxPOM.CoverFoxHomePage;
import coverFoxPOM.CoverFoxMemberDetailsPage;
import coverFoxUtility.Utility;

public class CF_TC555_Validate_search_results_for_healthcare_policies extends Base {

	public static Logger logger;
	CoverFoxHomePage home;
	CoverFoxHealthPlanPage healthPlan;
	CoverFoxAddressDetailsPage addressDetails;
	CoverFoxMemberDetailsPage memberDetails;
	CoverFoxHealthPlanResultsPage result;

	@BeforeClass
	public void launchBrowser() throws InterruptedException {
		logger = logger.getLogger("CoverFoxInsurance");
		PropertyConfigurator.configure("log4j.properties");

		launchCoverFox();
		logger.info("Launching CoverFox");
		home = new CoverFoxHomePage(driver);
		healthPlan = new CoverFoxHealthPlanPage(driver);
		addressDetails = new CoverFoxAddressDetailsPage(driver);
		memberDetails = new CoverFoxMemberDetailsPage(driver);
		result = new CoverFoxHealthPlanResultsPage(driver);

	}

	@BeforeMethod
	public void enterMemeberDeatils() throws InterruptedException, EncryptedDocumentException, IOException {

		home.clickOnMaleButton();
		logger.info("Clicking on male button");
		Thread.sleep(1000);

		healthPlan.clickOnNextButton();
		logger.info("clicking on next button");
		Thread.sleep(1000);

		logger.info("Handeling age drop down");
		memberDetails.hanldeAgeDropDown(Utility.readDataFromExcel(1, 0));
		logger.info("Clicking on next button");

		memberDetails.clickOnNextButton();
		Thread.sleep(1000);

		logger.info("Entering pin code");
		addressDetails.enterPinCode(Utility.readDataFromExcel(1, 1));
		logger.warn("Entering mobile num ");
		addressDetails.enterMobNum(Utility.readDataFromExcel(1, 2));
		logger.info("Clicking on continue button ");
		addressDetails.clickOnContinueButton();
		Thread.sleep(1000);

	}

	@Test
	public void validateTestPlansFromTextAndBanners() throws InterruptedException, IOException {
		Thread.sleep(5000);
		logger.error("Fetching number of results from text");
		int textResult = result.availablePlanNumberFromText();
		Thread.sleep(7000);
		logger.fatal("Fetching number of results from Banners ");
		int bannerResult = result.availablePlanNumberFromBanners();
		Thread.sleep(1000);
		Assert.assertEquals(textResult, bannerResult, "Text results are matching with Banner results, TC is failed");
		System.out.println(Utility.readDataFromPropertyFile("MobNum"));
		logger.error("TC is passed");

	}

	@AfterMethod
	public void closeBrowser() throws InterruptedException {

		Thread.sleep(3000);
		closeCoverFox();
	}
}
