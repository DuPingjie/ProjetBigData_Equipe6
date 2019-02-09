package info2.bigdata.mongodb;

import com.csvreader.CsvReader;
import com.mongodb.client.MongoCollection;

import java.io.IOException;
import java.nio.charset.Charset;

import org.bson.Document; 


public class DataReader {

		private String filePath; 
		private CsvReader r;
		
		public DataReader(String path) throws IOException {
			this.filePath=path;
			char decollator =',';
	        String encode = "GBK";	
			this.r = new CsvReader(filePath,decollator,Charset.forName(encode));			
		}
		
		public void insertToMongo(int row) throws IOException {
			
			r.readHeaders();
			String[] head = r.getHeaders(); //get heads
			System.out.println(head.length);

	        MongoDB mongo=new MongoDB("dataset");
	        MongoCollection<Document> data = mongo.mongoDatabase.getCollection("data");
	       
	        int j=0;
	        while (r.readRecord() && j<row)
	        {
	        	Document document=new Document();
	            for (int i = 0; i < head.length; i++)
	            {
	            	if(r.get(head[i])!="") {
	            	
						document.append(head[i], r.get(head[i]));
		               // System.out.println(head[i] + ":" + r.get(head[i]));
	            	}
	            }
            j++;
            data.insertOne(document);
            System.out.println(document);           
	        }    
	        r.close();    
	        //mongo.clear();
		}

}
	
	
	

	 



