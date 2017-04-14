import java.io.*;
import java.util.List;
import java.util.Map;
import java.util.Properties;

import edu.stanford.nlp.dcoref.CorefChain;
import edu.stanford.nlp.dcoref.CorefCoreAnnotations.CorefChainAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.LemmaAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.NamedEntityTagAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.PartOfSpeechAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.SentencesAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.TextAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.TokensAnnotation;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.semgraph.SemanticGraph;
import edu.stanford.nlp.semgraph.SemanticGraphCoreAnnotations.CollapsedCCProcessedDependenciesAnnotation;
import edu.stanford.nlp.trees.Tree;
import edu.stanford.nlp.trees.TreeCoreAnnotations.TreeAnnotation;
import edu.stanford.nlp.util.CoreMap;

public class StandfordTest {
    public static void main(String[] args) throws IOException {
        // 分句
//        String[] filelist = {"develop.txt", "train.txt"};
//        for (String file : filelist) {
//            if (file.indexOf("develop") != -1) {
//                String[] texts = read(file);
//                Passage(texts, 'd');
//            } else if (file.indexOf("train") != -1) {
//                String[] texts = read(file);
//                Passage(texts, 't');
//            }
//        }

        // 依存句法分析
//        String[] filelist = {"TrainDependSentence.txt", "DevelopDependSentence.txt"};
//        for (String file : filelist) {
//            String[] texts = read(file);
//            if (file.indexOf("Train") != -1) {
//                Dependency(texts, "train");
//            } else if (file.indexOf("Develop") != -1) {
//                Dependency(texts, "develop");
//            }
//        }

        // 关键词抽取
        String[] texts = read("keyword_sentence.txt");
        keyword(texts);
    }

    public static String[] read(String filename) {
        File file = new File(filename);
        Long filelength = file.length();
        byte[] filecontent = new byte[filelength.intValue()];
        try {
            FileInputStream in = new FileInputStream(file);
            in.read(filecontent);
            in.close();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

        String[] fileContentArr = new String(filecontent).split("\n");
        return fileContentArr;
    }

    public static void Passage(String[] texts, char flag) throws IOException {
        Properties props = new Properties();
        props.put("annotators", "tokenize, ssplit, pos, lemma, ner, parse, dcoref");
        StanfordCoreNLP pipeline = new StanfordCoreNLP(props);

        File out = null;
        if (flag == 't') {
            out = new File("TrainSet.txt");
        } else if (flag == 'd') {
            out = new File("DevelopSet.txt");
        }
        out.createNewFile();
        BufferedWriter output = new BufferedWriter(new FileWriter(out));

        for (String text : texts) {
            if (text.indexOf("passage") != -1 || text.indexOf("CID") != -1) {
                output.write(text + '\n');
                continue;
            }
            if (text.indexOf("title") != -1) {
                output.write("title:\n");
            } else if (text.indexOf("abstract") != -1) {
                output.write("abstract:\n");
            }

            Annotation document = new Annotation(text);
            pipeline.annotate(document);
            List<CoreMap> sentences = document.get(SentencesAnnotation.class);

            for (CoreMap sentence : sentences) {
                output.write(sentence.toString());
//                for (CoreLabel token : sentence.get(TokensAnnotation.class)) {
//                    String lemma = token.get(LemmaAnnotation.class);
//                    lemma = lemma.replace("-lrb-", "(").replace("-rrb-", ")").replace("-lsb-", "[").replace("-rsb-", "]");
//                    output.write(lemma + ' ');
//                }
                output.write("\n");
            }
        }
        output.flush();
        output.close();
    }

    public static void Dependency(String[] texts, String tag) throws IOException {
        Properties props = new Properties();
        props.put("annotators", "tokenize, ssplit, pos, lemma, ner, parse, dcoref");
        StanfordCoreNLP pipeline = new StanfordCoreNLP(props);

        File out;
        if (tag == "train") {
            out = new File("train_dependecny.txt");
        } else {
            out = new File("develop_dependency.txt");
        }
        out.createNewFile();
        BufferedWriter output = new BufferedWriter(new FileWriter(out));

        for (String text : texts) {
            if (text.indexOf("passage") != -1) {
                output.write(text + "\n");
            }
            else if(text == "\n"){
                output.write(text);
            }
            else {
                Annotation document = new Annotation(text);
                pipeline.annotate(document);

                List<CoreMap> sentences = document.get(SentencesAnnotation.class);
                for (CoreMap sentence : sentences) {
                    SemanticGraph dependencies = sentence.get(CollapsedCCProcessedDependenciesAnnotation.class);
                    output.write(dependencies.toString());
                }
            }
        }
        output.flush();
        output.close();
    }

    public static void keyword(String[] texts) throws IOException {
        Properties props = new Properties();
        props.put("annotators", "tokenize, ssplit, pos, lemma, ner, parse, dcoref");
        StanfordCoreNLP pipeline = new StanfordCoreNLP(props);

        File out = new File("keyword.txt");
        out.createNewFile();
        BufferedWriter output = new BufferedWriter(new FileWriter(out));

        for (String text : texts){
            Annotation document = new Annotation(text);
            pipeline.annotate(document);
            List<CoreMap> sentences = document.get(SentencesAnnotation.class);
            for (CoreMap sentence : sentences){
                for (CoreLabel token : sentence.get(TokensAnnotation.class)){
                    String lemma = token.get(LemmaAnnotation.class);
                    output.write(lemma+'\t');
                }
            }
            output.write('\n');
        }
        output.flush();
        output.close();
    }

    private static void complete() {
        // creates a StanfordCoreNLP object, with POS tagging, lemmatization, NER, parsing, and coreference resolution
        Properties props = new Properties();
        props.put("annotators", "tokenize, ssplit, pos, lemma, ner, parse, dcoref");
        StanfordCoreNLP pipeline = new StanfordCoreNLP(props);

        // read some text in the text variable
        String text = "435349\t395\t409\tFasciculations\tDisease\tD005207";

        // create an empty Annotation just with the given text
        Annotation document = new Annotation(text);

        // run all Annotators on this text
        pipeline.annotate(document);

        // these are all the sentences in this document
        // a CoreMap is essentially a Map that uses class objects as keys and has values with custom types
        List<CoreMap> sentences = document.get(SentencesAnnotation.class);

        System.out.println("word\t\tpos\t\tlemma\t\tner");
        for (CoreMap sentence : sentences) {
            // traversing the words in the current sentence
            // a CoreLabel is a CoreMap with additional token-specific methods
            for (CoreLabel token : sentence.get(TokensAnnotation.class)) {
                // this is the text of the token
                String word = token.get(TextAnnotation.class);
                // this is the POS tag of the token
                String pos = token.get(PartOfSpeechAnnotation.class);
                // this is the NER label of the token
                String ne = token.get(NamedEntityTagAnnotation.class);
                String lemma = token.get(LemmaAnnotation.class);

                System.out.println(word + "\t\t" + pos + "\t\t" + lemma + "\t\t" + ne);
            }
            // this is the parse tree of the current sentence
            Tree tree = sentence.get(TreeAnnotation.class);
            System.out.println(tree);
            // this is the Stanford dependency graph of the current sentence
            SemanticGraph dependencies = sentence.get(CollapsedCCProcessedDependenciesAnnotation.class);
            System.out.println(dependencies);
        }
        // This is the coreference link graph
        // Each chain stores a set of mentions that link to each other,
        // along with a method for getting the most representative mention
        // Both sentence and token offsets start at 1!
        Map<Integer, CorefChain> graph = document.get(CorefChainAnnotation.class);
        System.out.println(graph);
    }

}