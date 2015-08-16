Title: Processing whole files from S3 with Spark
Date: 2015-02-11
Tags: spark, how-to
Slug: processing-whole-files-spark-s3

I have recently started diving into [Apache Spark](https://spark.apache.org/) for a project at work and ran into issues trying to process the contents of a collection of files in parallel, particularly when the files are stored on Amazon S3. In this post I describe my problem and how I got around it.

My first Spark project is simple. I have a single function that processes data from a file and a lot of data files to process using this function. It should be trivial to distribute this task, right? Just create an RDD (Spark's core data container, basically a distributed collection whose items can be operated on in parallel) where each item contains the contents of a single file and apply my function using the RDD methods `foreach` or `map` if I want to capture results for logging or something. 

Most examples I found for `pyspark` create RDDs using the `SparkContext.textFile()` method. This generates an RDD where each line of the file is an item in the collection. This is not what I want. Looking through the API docs I found the method `SparkContext.wholeTextFiles()` that appears to do exactly what I want. I can point this method to a directory and it will create an RDD where each item contains data from an entire file. Perfect! Well, it would be if it worked anyway.

Here's the issue... our data files are stored on Amazon S3, and for whatever reason this method fails when reading data from S3 (using Spark v1.2.0). I'm using [`pyspark`](https://spark.apache.org/docs/1.2.1/api/python/pyspark.html) but I've read in forums that people are having the same issue with the Scala library, so it's not just a Python issue. Anyway, here's how I got around this problem.

First, I create a listing of files in a root directory and store the listing in a text file in a scratch bucket on S3. Here is a code snippet (I'm using [`boto`](https://boto.readthedocs.org/en/latest/) to interact with S3):

    :::python
    conn = boto.connect_s3()
    # bucket is the name of the S3 bucket where your data resides
    b = conn.get_bucket(bucket)  
    # inkey_root is the S3 'directory' in which your files are located
    keys = b.list(prefix=inkey_root)  
    
    key_list = [key.name for key in keys]
    
    conn.close()

Next I need a function that takes a file path, parses the data from the file into a string, and returns a tuple with the file name and contents (as a string). Here is just such a function:

    :::python
    def fetch_data(s3key):
        """
        Fetch data with the given s3 key and pass along the contents as a string.
    
        :param s3key: An s3 key path string.
        :return: A tuple (file_name, data) where data is the contents of the 
            file in a string. Note that if the file is compressed the string will 
            contain the compressed data which will have to be unzipped using the 
            gzip package.
        """
        conn = boto.connect_s3()
        b = conn.get_bucket(bucket)
        k = b.get_key(s3key)
        data = k.get_contents_as_string()
        conn.close()
        
        # I use basename() to get just the file name itself
        return os.path.basename(s3key), data

Then I create an RDD using `parallelize` on the listing of files to process. The RDD items will be the paths (ok fine, *keys*) of the files that I want to process in S3.  Then I call the RDD's `map` method, using `fetch_data` to parse the files and pass their contents along as a new RDD with the file contents as items, just like I wanted from `wholeTextFiles` in the first place. Then you can go ahead and process the resulting data as necessary, e.g. by chaining a call to another `map`, `foreach` or whatever. Here's the code, with a chained call to `foreach` to process the data using a function `process_data`.
    
    :::python
    sc = pyspark.SparkContext('local', 'Whatever')
    # Create an RDD from the list of s3 key names to process stored in key_list
    file_list = sc.parallelize(key_list)
    file_list.map(fetch_data).foreach(process_data)

So there you have it, a simple way to get around the fact that Spark's `wholeTextFiles` (as of now) does not work with files stored in S3.