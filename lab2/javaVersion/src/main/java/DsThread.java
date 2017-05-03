/**
 * Created by lucas_menezes on 27/04/17.
 */
class DsThread extends Thread {
    int threadId;
    MessageStructure threadMessage;


    DsThread(int threadId, MessageStructure message){
        this.threadId = threadId;
        this.threadMessage = message;
    }

    @Override
    public void run() {
        synchronized(threadMessage) {
            while (threadMessage.checkIfIsDone()){
                if (!MessageStructure.available.get()) {
                    MessageStructure.available.set(true);

                    System.out.println(threadMessage.getMessage());

                    threadMessage.uppercaseCharacter();
                    try {
                        Thread.sleep(500);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                    MessageStructure.available.set(false);
                }
            }
        }
    }








}

