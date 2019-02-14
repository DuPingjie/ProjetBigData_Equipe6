package info2.bigdata.mongodb;

import java.io.IOException;

public class Main {
	public static void main(String[] args) throws IOException {    
		
		DataReader dr=new DataReader ("src/main/resources/predict.csv");
		dr.insertToMongo(300000); // parameter: the number of lines to insert (1 - 300000)
		System.out.println("Data have been put in MongoDB successfully!");
	}

}
