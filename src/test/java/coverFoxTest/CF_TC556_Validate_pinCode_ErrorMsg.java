package coverFoxTest;

import java.io.IOException;

import org.apache.commons.math3.analysis.function.Add;
import org.apache.log4j.Logger;
import org.apache.log4j.PropertyConfigurator;
import org.apache.poi.EncryptedDocumentException;
import org.apache.poi.ss.formula.functions.Address;
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
import coverFoxPOM.CoverFoxHomePage;
import coverFoxPOM.CoverFoxMemberDetailsPage;
import coverFoxUtility.Utility;

public class CF_TC556_Validate_pinCode_ErrorMsg extends Base {
	public static Logger logger;

	CoverFoxHomePage home;
	CoverFoxHealthPlanPage healthPlan;
	CoverFoxMemberDetailsPage memberDetails;
	CoverFoxAddressDetailsPage adress;

	@BeforeClass
	public void launchBrowser() throws InterruptedException {
//		logger= logger.getLogger("CoverFoxInsurance");
//		PropertyConfigurator.configure("log4j.properties");
		launchCoverFox();
		home = new CoverFoxHomePage(driver);
		healthPlan = new CoverFoxHealthPlanPage(driver);
		memberDetails = new CoverFoxMemberDetailsPage(driver);
		adress = new CoverFoxAddressDetailsPage(driver);

	}

	@BeforeMethod
	public void enterMemeberDeatils() throws InterruptedException, EncryptedDocumentException, IOException {
		home.clickOnMaleButton();

		Thread.sleep(1000);
		healthPlan.clickOnNextButton();
		Thread.sleep(1000);
		memberDetails.hanldeAgeDropDown(Utility.readDataFromExcel(1, 0));
		memberDetails.clickOnNextButton();
		Thread.sleep(1000);
		adress.enterMobNum(Utility.readDataFromExcel(1, 2));
		Thread.sleep(1000);
		adress.clickOnContinueButton();
		Thread.sleep(1000);
	}

	@Test
	public void validate_pinCode_ErrorMsg() {
		Reporter.log("Validating pinCode Error msg", true);
		boolean result = adress.validateErrorPinErrorMsg();
		Assert.assertTrue(result, "Pin Code error msg is not displayed, TC is failed");
		Reporter.log("TC is passed", true);

	}

	@AfterMethod
	public void closeBrowser() throws InterruptedException {
		Thread.sleep(4000);
		closeCoverFox();
	}
}
