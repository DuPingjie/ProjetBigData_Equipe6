package info2.bigdata.mongodb;


import com.mongodb.MongoClient;
import com.mongodb.client.MongoDatabase;

public class MongoDB {


	public MongoClient mongoClient;
	public MongoDatabase mongoDatabase;
	
	public MongoDB(String db_name) {

		try {

			// Connect to MongoDB
			this.mongoClient = new MongoClient("localhost", 27017);

			// Connect to database
			this.mongoDatabase = mongoClient.getDatabase(db_name);
			System.out.println("Connect to database successfully");
			mongoDatabase.createCollection("predict");
			System.out.println("Collection data is created!");
			
		} 
		catch (Exception e) {
			System.err.println(e.getClass().getName() + ": " + e.getMessage());
		}
		
	}
	
	public void clear() {
		// Drop database
		mongoDatabase.drop();		
		
	}

}
