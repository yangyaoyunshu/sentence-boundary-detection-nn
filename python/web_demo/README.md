# Run Demo

As described in the [general Python README](../README.md), before executing any scripts on the server, please execute the following command  `. ./use_python p2`  in `/home/ms2015t3/sentence-boundary-detection-nn`.

```
cd /home/ms2015t3/sentence-boundary-detection-nn
. ./use_python p2
```
 
Then use the following command on the server to run the demo:

 `python web_demo/web.py /home/ms2015t3/demo_data /home/fb10dl01/workspace/ms-2015-t3/GoogleNews-vectors-negative300.bin -nd`

Or the equivalent for your specific environment:

 `python web_demo/web.py [DemoDataFolder] [TrainedWord2VecModel] -nd`

