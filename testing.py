from feature_groups import *
from data import ShortAnswerInstance

header = ['taskId','itemId','itemPrompt',' itemTargets','learnerId','answer', 'label']

def parse_instances(filename):
    return pd.read_csv(filename,
                         dtype={'taskId':str,'itemId':str,'itemPrompt':str,' itemTargets':str,'learnerId':str,'answer':str,
                                'label':str}, encoding='utf8', sep="\t")

if __name__ == '__main__':
    taskId = 'ID1'
    itemId = 'EF123'
    itemPrompt = 'What is the capital of Germany?'
    itemTargets = ['Berlin']
    learnerId = 'XYZ01'
    answer = 'Berlin'
    label = '1.0'

    data=parse_instances('testing_data/feedbook_data_with_gec.tsv').iloc[0:5]
    data.to_csv("test.tsv", sep='\t', encoding='utf8')

    # create a dummy instance for each row
    data_as_instances = []
    print(data.columns)
    for row in data.iterrows():
        print(row)
        print(row['taskId'])
        d = ShortAnswerInstance(taskId=row['taskId'], itemId=row['itemId'], itemPrompt=row['itemPrompt'],
                                itemTargets=row['itemTargets'], learnerId=row['learnerId'],
                                answer=row['answer'], label=row['label'])
        data_as_instances.append(d)
        print(d.answer)

    # extract features
    #bow_extractor = BOWGroupExtractor()
    #bow_extractor.extract(data_as_instances)