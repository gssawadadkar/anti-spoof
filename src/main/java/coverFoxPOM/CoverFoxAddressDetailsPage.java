package coverFoxPOM;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;
import org.testng.Reporter;

public class CoverFoxAddressDetailsPage 
{
	
	@FindBy(xpath = "(//input[@type='number'])[1]") private WebElement pinCodeField;
	@FindBy(xpath = "(//input[@type='number'])[2]") private WebElement mobNumField;
	@FindBy(xpath = "//div[text()='Continue']") private WebElement continueButton;
	@FindBy(xpath = "//div[contains(text(),'valid pincode')]") private WebElement pinCodeErrorMsg;
	
	
	
	public CoverFoxAddressDetailsPage(WebDriver driver)
	{
		PageFactory.initElements(driver, this);
	}
	
	public void enterPinCode(String pincode)
	{
		pinCodeField.sendKeys(pincode);
	}
	
	public void enterMobNum(String mobNum)
	{
		Reporter.log("Entering mobile Num..", false);
		mobNumField.sendKeys(mobNum);
	}
	
	public void clickOnContinueButton()
	{
		continueButton.click();
	}
	
	public boolean validateErrorPinErrorMsg()
	{
		boolean result = pinCodeErrorMsg.isDisplayed();
		return result;
	}
	
}
