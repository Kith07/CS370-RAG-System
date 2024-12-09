# CS370-RAG-System

To build a RAG system that can be used by an ROS2 robotics developer to develop the navigation stack of an agent with egomotion. This means that robotics is the domain, but the system must be particularly helpful (able to answer very specific questions about the subdomains).

## 1. Environment and Tooling Milestone

Delivered a `docker-compose` file that will create a development environment for the RAG system. The environment contains the following components:

1. **app**:  
   - Can train and serve PyTorch or TensorFlow/Keras models.  
   - Interacts with the Hugging Face Hub API.  
   - Encapsulates all subcomponents that are not infrastructure.

2. **mongodb**:  
   - Database for storing the RAG raw data after the ETL pipeline.

3. **qdrant**:  
   - The vector search engine for the RAG system.

4. **clearml**:  
   - The orchestrator and experiment tracking system for the RAG system.  
   - Please note that the book is using ZenML.

![All Docker Containers Running]("Screenshots/dockerps.png")

## 2. ETL Milestone

While we were able to have the ClearML container up and running on our local server, we were unable to incorporate ClearML's orchestrator into our existing code for the ETL Pipeline. As such, we had to manually ingest the links all of the data we found regarding the specific subdomains so we could move forward with the rest of the project. That said, our ETL pipeline still accomplishes all of the expected tasks such as using web crawlers to gather informaation from github repos and youtube videos related to the subdomains, followed by ingesting the raw data alongside its metdata into our MongoDB database, also running locally. Below is a screenshot after printing some (Too Many for One Screenshot) of the explicitly ingested URLs:

![All Ingested URLs into MongoDB]("Screenshots/ingestedUrls.png")

## 3. Featurization Pipelines Milestone

We succesfully implemented this pipeline to create featurized vectors from our raw data. Our implementation involved the following steps:

1. Retreive our raw data stored in the MongoDB database
2. Format it into JSON using a separate custom JSON Class
3. Reformat the JSON File to allow for insertion into Qdrant Database
4. Test creating embedded vectors
5. Appending all of the vector embeddings alongside an id and its metadata containing the title, platform, and link of each source into the Qdrant Vector Search Engine

![All Ingested URLs into MongoDB]("Screenshots/qdrant_ingest.png")

## 4. Finetuning Milestone
Custom trained LLama 3.1 Model using QnA pairs we created by asking for intensive questions about the subdomains using a GPT model. 

## 5. Deploying the App Milestone
Deployed the Gradio Application using LLama3.1 for the generation/LLM model(Finetuned) and OpenAI GPT-3.5 for the embedding model.

![Example Output for Gradio App]("Screenshots/gradioImage.png")
