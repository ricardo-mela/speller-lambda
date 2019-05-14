#! /usr/bin/env python

from random import shuffle
import boto3
import botocore
def lambda_handler(event,context):
  s3 = boto3.resource('s3')
  obj = s3.Object('bucket-name','text.txt')
  in_file = obj.get()['Body'].read().decode('utf-8')
  print in_file
  words = in_file.splitlines()
  text = '<speak>'
  text += ' Hello <lang xml:lang="es-MX">Agustin</lang>, these are your spelling words for this week.<break time="3s"/>'
    
  shuffle(words)

  i = 0
  while i < len(words):
      break_time = len(words[i])
      text += words[i]+', <break time="2s"/>'+words[i]+'<break time="'+str(break_time)+'s"/>,'
      i += 1

  text +='</speak>'


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
  return {
    "Text": text
  }
