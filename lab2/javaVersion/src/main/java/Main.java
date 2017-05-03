import java.util.ArrayList;

/**
 * Created by lucas_menezes on 27/04/17.
 *
 */

public class Main {
    public static void main(String[] args) throws InterruptedException {
        ArrayList<Thread> threadsList = new ArrayList();
        int numberOfThreads = 30;
        Thread thread;

        MessageStructure messageData = new MessageStructure();

        for (int i = 1; i <= numberOfThreads; i++) {

            thread = new DsThread(i, messageData);
            thread.start();
            threadsList.add(thread);
        }

        MessageStructure.available.set(false);

        for (Thread t : threadsList) {
            t.join();
        }
    }
}
