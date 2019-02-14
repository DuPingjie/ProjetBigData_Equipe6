import java.io.IOException;

import org.junit.Test;

import info2.bigdata.mongodb.DataReader;
import junit.framework.TestCase;

public class test extends TestCase { 
		
     @Test
     public void testMain() {

		try {
			DataReader dr = new DataReader ("src/main/resources/predict.csv");// or the dadaset.csv for testing the original data
			dr.insertToMongo(300000);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
 		System.out.println("Data have been put in MongoDB successfully!");
 	 }
}
