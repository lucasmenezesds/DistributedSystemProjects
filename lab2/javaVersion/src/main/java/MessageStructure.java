import java.util.concurrent.atomic.AtomicBoolean;

/**
 * Created by lucas_menezes on 27/04/17.
 */
class MessageStructure {
    private static String message = "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzab";
    private int messageSize;
    private int position = 0;
    public static AtomicBoolean available = new AtomicBoolean(true);


    public synchronized String getMessage() {
        return message;
    }

    public synchronized int getMessageSize() {
        return messageSize = this.message.length();
    }

    public synchronized void nextPosition(){
        this.position += 1;
    }

    public synchronized void uppercaseCharacter() {
        String myMessage = this.message;
        char[] myMessageArray = myMessage.toCharArray();
        char selectedChar = myMessageArray[this.position];
        String convertedChar = String.valueOf(selectedChar).toUpperCase();

        StringBuilder myMessageBuillded = new StringBuilder(myMessage);
        this.message = myMessageBuillded.replace(this.position, this.position + 1, convertedChar).toString();

        System.out.println(this.getMessage());

        nextPosition();
    }

    public synchronized boolean checkIfIsDone(){
        if(this.position >= this.getMessageSize()){
//            System.out.println("All the string is uppercased: " + this.message);
            return false;
        } else {
//            System.out.println("The string until now is like:" + this.message);
            return true;
        }
    }

}