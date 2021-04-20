Must run program with 5 command line arguments
    2 must be DNA/Protein sequences that are in FASTA format
    1 must be the character l, g, or s, to determine how we will be aligning them
    1 must be t or f, t if we are working with proteins, f if we are working with DNA
    1 must be the output file that we will be writing our info to
If these conditions are not met then you will get an error

Once we provide correct arguments we will first call the createScoreMatrix function
where we will be reading a matrix file based upon whether we are workin on DNA or protein sequences
We will read the file and generate a scoring matrix to refernce in order to create a sequence alignment Score

We then align the sequences by calling the alignSequences function. Here we read the prvodided sequence
files and compare them by characters. We get three values and we choose the best value to be applied to our matrix 
that is the length sequence 1 x length of sequence 2. After going through every character in both sequences we return 
the matrix and other important values

We then call our writeFile function which writes to a file containg the new sequences and the score. We back track 
to the begining of our matrix with the use of our dictioanry we created in the first funtion. The dictioanry's key 
is the current postion and the value is the next position that leads us to the next location that brings us to the 
start of our matrix. Based upon the direction we go to, up left, or diagnal, we will add a charcater or a gap into 
our new sequence. We do this process until we reach the begining of our matrix. When completed we write the important 
data to a new file, we write the new sequences, the score they recieved, the matches we have, and where the sequences
start and end.

