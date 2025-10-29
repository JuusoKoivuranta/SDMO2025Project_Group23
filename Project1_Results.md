
# PROJECT 1
Starting point for the project was applying the provided implementation of the Bird heuristic.

Chosen GitHub repositories for project 1 were:

### ShiftMediaProject FFmpeg: 

(https://github.com/dspsir/SMP-FFmpeg), GitHub claims 1,013 unique contributors and 95,052 commits.

Using the Bird heuristic at 90 % treshold with these repositories produced a true positive / false positive rate in the case of ShiftMediaProject FFmpeg:

Total Pairs: 830

#### Manual Review found the following results:

True positives: 508 (61,12 %)
                            
False positives: 322 (38,79 %)
                            
This is a very bad ratio!

### [OTHER REPOSITORY]:



## Alternative Method:
As an alternative to the Bird heuristic algorithm we will study if a Language Model (LM) will be able to achieve a better true / false positive percentage this way. We will use LM Studio (https://lmstudio.ai/) as a LM tool to contact the model and we will be specifically be using Openai's gpt-oss-20b model.

It is important that the user knows the technical limitations of their device because this method is a much more time-consuming and requires high system performance due to large resource demands.

### Results using alternative method

FFmpeg: Total Pairs: 60

#### Manual Review found the following results:

True positives: 59 (98,33 %)
                            
False positives: 1 (1,66 %)
                            
This is a much better ratio! However there seems to be multiple duplicates that the llm did not flag as a possible duplicate when we compare to the Bird heuristic (508 - 59 = 449). This can possible be optimised with making the given prompt more accurate, but even then it probably could not detect every possible pair.