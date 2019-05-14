#! /usr/bin/env python

from random import shuffle
import boto3

words = []
text = '<speak>'
text += ' Hello <lang xml:lang="es-MX">Agustin</lang>, these are your spelling words for this week.<break time="3s"/>'
with open('myfile.txt') as fp:
  for line in fp:
    line.rstrip()
    words.append(line)
    
shuffle(words)

i = 0
while i < len(words):
    break_time = len(words[i])
    text += words[i]+', <break time="2s"/>'+words[i]+'<break time="'+str(break_time)+'s"/>,'
    i += 1

text +='</speak>'

print text

polly = boto3.client('polly')

response = polly.synthesize_speech(VoiceId='Joanna',
                OutputFormat='mp3',
                TextType='ssml',
                LanguageCode='en-GB', 
                Text = text)

recording = response['AudioStream'].read()

s3 = boto3.resource('s3')
audio = s3.Object('bucket-name','speech.mp3')
audio.put(Body=recording)

#file = open('speech.mp3', 'w')
#file.write(response['AudioStream'].read())
#file.close()
