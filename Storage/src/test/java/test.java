import java.io.IOException;

import org.junit.Test;

import info2.bigdata.mongodb.DataReader;
import junit.framework.TestCase;

public class test extends TestCase { 
		
     @Test
     public void testMain() {

		try {
			DataReader dr = new DataReader ("src/main/resources/dataset.csv");
			dr.insertToMongo(300000);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
 		System.out.println("Data have been put in MongoDB successfully!");
 	 }
}
