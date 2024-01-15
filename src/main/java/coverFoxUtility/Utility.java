package coverFoxUtility;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Properties;
import java.util.logging.FileHandler;

import org.apache.poi.EncryptedDocumentException;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.WorkbookFactory;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.io.*;
import org.testng.Reporter;

public class Utility 
{
	public static String readDataFromExcel(int row, int cell) throws EncryptedDocumentException, IOException
	{
		Reporter.log("Reading data from excelSheet", true);
		FileInputStream myfile= new FileInputStream(System.getProperty("user.dir")+"\\src\\test\\resources\\29JulyEvenTest.xlsx");
			
		Sheet mySheet = WorkbookFactory.create(myfile).getSheet("CoverFoxData");
		String data = mySheet.getRow(row).getCell(cell).getStringCellValue();
		return data;
	}
	public static String takeScreenShot(WebDriver driver,String TCID) throws IOException
	{
		Reporter.log("Taking screenshot", true);
		String timeStamp=  new SimpleDateFormat("yyyy.MM.dd.HH.mm.ss").format(new Date());
		File src = ((TakesScreenshot)driver).getScreenshotAs(OutputType.FILE);
		//String path="D:\\Velocity\\Java Class\\29th July Even\\screenShot\\coverFox";
		
		String destination = System.getProperty("user.dir") + "/ScreenShot/"  +TCID+timeStamp+".png";
//		File dest= new File(destination);
//	
//		
//		File dest=new File("D:\\Velocity\\Java Class\\29th July Even\\screenShot\\coverFox"+TCID+"_"+timeStamp+".png");
		Reporter.log("Saved screenshot at "+destination, true);
		org.openqa.selenium.io.FileHandler.copy(src, new File(destination));
		return destination;
	}
	
	public static String readDataFromPropertyFile(String key) throws IOException
	{
		//Create object of Properties class
		Properties prop= new Properties();
		//File Location
		FileInputStream myFile= new FileInputStream(System.getProperty("user.dir")+"//CoverFoxData.properties");
		//load file
		prop.load(myFile);
		//pass the Key for the data we want
		String value = prop.getProperty(key);
		return value;
	}

}
