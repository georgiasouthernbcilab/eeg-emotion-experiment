#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2023.2.3),
    on March 25, 2024, at 13:41
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import plugins
plugins.activatePlugins()
prefs.hardware['audioLib'] = 'ptb'
prefs.hardware['audioLatencyMode'] = '3'
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout
from psychopy.tools import environmenttools
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER, priority)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

import psychopy.iohub as io
from psychopy.hardware import keyboard
from psychopy.hardware import emotiv
from psychopy.hardware import camera
from psychopy.sound import microphone

# Run 'Before Experiment' code from code
import subprocess

def capture_webcam(filename):
    # Command to capture webcam using ffmpeg on Windows
    print('filename',filename)
    ffmpeg_cmd = [
        'ffmpeg',
        '-f', 'dshow',                     # Input format (DirectShow)
        '-i', 'video=Logitech HD Webcam C510', # Specify the webcam device name here
        '-c:v', 'libxvid',                 # Video codec (Xvid)
        '-q:v', '5',                       # Video quality (lower is better quality, range 1-31)
        filename+'.avi'      # Output file
    ]
   
    # Start the subprocess
    ffmpeg_process = subprocess.Popen(ffmpeg_cmd)
   
    # Return the subprocess object
    return ffmpeg_process

# Call the function to start capturing webcam
# ffmpeg_process = capture_webcam()

trialsList = []
neutralVideos = []
selectionTrialsList = []
experimentTrialsList = []
categoryIndex = 0
moviePath = None
fileLocation = ''

for video in os.listdir('neutral_videos'):
    videoPath = os.path.join('neutral_videos',video)
    neutralVideos.append(videoPath)

for category in os.listdir('videos'):

    thisSelectionTrialDict = {
    'mainIndex': categoryIndex, 'emotion':category,
    'image1': None, 'text1': '', 'stimuli1': None, 
    'image2': None, 'text2': '', 'stimuli2': None, 
    'image3': None, 'text3': '', 'stimuli3': None
    }

    fullpath = os.path.join('videos',category)
    emotion=category.split()[1]
    categoryName = category.split()[1]
    thisTrialDict = {
    'mainIndex':categoryIndex,
    'stim': '',
    'emotion': categoryName, 
    'neutralvideo': neutralVideos[categoryIndex]
    }
    
    if (len(os.listdir('videos/'+category)))==1:
        fileLocation = ''
        for file in os.listdir('videos/'+category):
            filename, extension = os.path.splitext(file)
            fileLocation = os.path.join(fullpath,file)
            if extension == '.mp4':
                moviePath = os.path.join(fullpath,item)
                print('    movie path',fileLocation,end='')
                thisTrialDict['stim']=fileLocation

            if extension == '.mkv':
                moviePath = os.path.join(fullpath,item)
                print('    movie path',fileLocation,end='')
                thisTrialDict['stim']=fileLocation
        
    if (len(os.listdir('videos/'+category)))>1:
        stim = 1
        
        for subcategory in os.listdir('videos/'+category):
            fullpath =os.path.join('videos',category,subcategory)
            thisSelectionTrialDict['text'+str(stim)]=subcategory.split()[1]
            
            for item in os.listdir(fullpath):
                filename, extension = os.path.splitext(item)
                
                if extension == '.mp4':
                    moviePath = os.path.join(fullpath,item)
                    thisSelectionTrialDict['stimuli'+str(stim)]=moviePath

                if extension == '.mkv':
                    moviePath = os.path.join(fullpath,item)
                    thisSelectionTrialDict['stimuli'+str(stim)]=moviePath

                elif extension == '.jpg':
                    imagePath = os.path.join(fullpath,item)
                    thisSelectionTrialDict['image'+str(stim)]=imagePath

            stim+=1
    
        selectionTrialsList.append(thisSelectionTrialDict)

    categoryIndex +=1
    experimentTrialsList.append(thisTrialDict)   
print('selectionTrialsList',selectionTrialsList)
# Run 'Before Experiment' code from code_2
# Code inserted in positivenegative, before experiment section
# --- Setup global variables (available in all functions) ---
# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
# Store info about the experiment session
psychopyVersion = '2023.2.3'
expName = 'emotionRecognition'  # from the Builder filename that created this script
expInfo = {
    'participant': f"{randint(0, 999999):06.0f}",
    'session': '001',
    'Ethnicity': '',
    'Gender': '',
    'Age': '',
    'date': data.getDateStr(),  # add a simple timestamp
    'expName': expName,
    'psychopyVersion': psychopyVersion,
}


def showExpInfoDlg(expInfo):
    """
    Show participant info dialog.
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    
    Returns
    ==========
    dict
        Information about this experiment.
    """
    # temporarily remove keys which the dialog doesn't need to show
    poppedKeys = {
        'date': expInfo.pop('date', data.getDateStr()),
        'expName': expInfo.pop('expName', expName),
        'psychopyVersion': expInfo.pop('psychopyVersion', psychopyVersion),
    }
    # show participant info dialog
    dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
    if dlg.OK == False:
        core.quit()  # user pressed cancel
    # restore hidden keys
    expInfo.update(poppedKeys)
    # return expInfo
    return expInfo


def setupData(expInfo, dataDir=None):
    """
    Make an ExperimentHandler to handle trials and saving.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    dataDir : Path, str or None
        Folder to save the data to, leave as None to create a folder in the current directory.    
    Returns
    ==========
    psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    
    # data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    if dataDir is None:
        dataDir = _thisDir
    filename = u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])
    # make sure filename is relative to dataDir
    if os.path.isabs(filename):
        dataDir = os.path.commonprefix([dataDir, filename])
        filename = os.path.relpath(filename, dataDir)
    
    # an ExperimentHandler isn't essential but helps with data saving
    thisExp = data.ExperimentHandler(
        name=expName, version='',
        extraInfo=expInfo, runtimeInfo=None,
        originPath='C:\\Users\\mw24396\\Desktop\\eegTest\\testomgmeweeg.py',
        savePickle=True, saveWideText=True,
        dataFileName=dataDir + os.sep + filename, sortColumns='time'
    )
    thisExp.setPriority('thisRow.t', priority.CRITICAL)
    thisExp.setPriority('expName', priority.LOW)
    # return experiment handler
    return thisExp


def setupLogging(filename):
    """
    Setup a log file and tell it what level to log at.
    
    Parameters
    ==========
    filename : str or pathlib.Path
        Filename to save log file and data files as, doesn't need an extension.
    
    Returns
    ==========
    psychopy.logging.LogFile
        Text stream to receive inputs from the logging system.
    """
    # this outputs to the screen, not a file
    logging.console.setLevel(logging.EXP)
    # save a log file for detail verbose info
    logFile = logging.LogFile(filename+'.log', level=logging.EXP)
    
    return logFile


def setupWindow(expInfo=None, win=None):
    """
    Setup the Window
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    win : psychopy.visual.Window
        Window to setup - leave as None to create a new window.
    
    Returns
    ==========
    psychopy.visual.Window
        Window in which to run this experiment.
    """
    if win is None:
        # if not given a window to setup, make one
        win = visual.Window(
            size=[1680, 1050], fullscr=True, screen=0,
            winType='pyglet', allowStencil=False,
            monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
            backgroundImage='', backgroundFit='none',
            blendMode='avg', useFBO=True,
            units='pix'
        )
        if expInfo is not None:
            # store frame rate of monitor if we can measure it
            expInfo['frameRate'] = win.getActualFrameRate()
    else:
        # if we have a window, just set the attributes which are safe to set
        win.color = [0,0,0]
        win.colorSpace = 'rgb'
        win.backgroundImage = ''
        win.backgroundFit = 'none'
        win.units = 'pix'
    win.mouseVisible = False
    win.hideMessage()
    return win


def setupInputs(expInfo, thisExp, win):
    """
    Setup whatever inputs are available (mouse, keyboard, eyetracker, etc.)
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window in which to run this experiment.
    Returns
    ==========
    dict
        Dictionary of input devices by name.
    """
    # --- Setup input devices ---
    inputs = {}
    ioConfig = {}
    
    # Setup iohub keyboard
    ioConfig['Keyboard'] = dict(use_keymap='psychopy')
    
    ioSession = '1'
    if 'session' in expInfo:
        ioSession = str(expInfo['session'])
    ioServer = io.launchHubServer(window=win, **ioConfig)
    eyetracker = None
    
    # create a default keyboard (e.g. to check for escape)
    defaultKeyboard = keyboard.Keyboard(backend='iohub')
    # return inputs dict
    return {
        'ioServer': ioServer,
        'defaultKeyboard': defaultKeyboard,
        'eyetracker': eyetracker,
    }

def pauseExperiment(thisExp, inputs=None, win=None, timers=[], playbackComponents=[]):
    """
    Pause this experiment, preventing the flow from advancing to the next routine until resumed.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    inputs : dict
        Dictionary of input devices by name.
    win : psychopy.visual.Window
        Window for this experiment.
    timers : list, tuple
        List of timers to reset once pausing is finished.
    playbackComponents : list, tuple
        List of any components with a `pause` method which need to be paused.
    """
    # if we are not paused, do nothing
    if thisExp.status != PAUSED:
        return
    
    # pause any playback components
    for comp in playbackComponents:
        comp.pause()
    # prevent components from auto-drawing
    win.stashAutoDraw()
    # run a while loop while we wait to unpause
    while thisExp.status == PAUSED:
        # make sure we have a keyboard
        if inputs is None:
            inputs = {
                'defaultKeyboard': keyboard.Keyboard(backend='ioHub')
            }
        # check for quit (typically the Esc key)
        if inputs['defaultKeyboard'].getKeys(keyList=['escape']):
            endExperiment(thisExp, win=win, inputs=inputs)
        # flip the screen
        win.flip()
    # if stop was requested while paused, quit
    if thisExp.status == FINISHED:
        endExperiment(thisExp, inputs=inputs, win=win)
    # resume any playback components
    for comp in playbackComponents:
        comp.play()
    # restore auto-drawn components
    win.retrieveAutoDraw()
    # reset any timers
    for timer in timers:
        timer.reset()


def run(expInfo, thisExp, win, inputs, globalClock=None, thisSession=None):
    global ffmpeg_process
    """
    Run the experiment flow.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    psychopy.visual.Window
        Window in which to run this experiment.
    inputs : dict
        Dictionary of input devices by name.
    globalClock : psychopy.core.clock.Clock or None
        Clock to get global time from - supply None to make a new one.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    # mark experiment as started
    thisExp.status = STARTED
    # make sure variables created by exec are available globally
    exec = environmenttools.setExecEnvironment(globals())
    # get device handles from dict of input devices
    ioServer = inputs['ioServer']
    defaultKeyboard = inputs['defaultKeyboard']
    eyetracker = inputs['eyetracker']
    # make sure we're running in the directory for this experiment
    os.chdir(_thisDir)
    # get filename from ExperimentHandler for convenience
    filename = thisExp.dataFileName
    ffmpeg_process = capture_webcam(thisExp.dataFileName)
    frameTolerance = 0.001  # how close to onset before 'same' frame
    endExpNow = False  # flag for 'escape' or other condition => quit the exp
    # get frame duration from frame rate in expInfo
    if 'frameRate' in expInfo and expInfo['frameRate'] is not None:
        frameDur = 1.0 / round(expInfo['frameRate'])
    else:
        frameDur = 1.0 / 60.0  # could not measure, so guess
    
    # Start Code - component code to be run after the window creation
    # This is generated by the writeStartCode
    # This is generated by the writeStartCode
    # This is generated by the writeStartCode
    
    # --- Initialize components for Routine "chooseCategoriesTrial" ---
    instructions = visual.TextStim(win=win, name='instructions',
        text="Please select your prefered category from the choices below",
        font='Arial',
        pos=(0,win.size[1]/2.5), height=40.0, wrapWidth=(win.size[0]/1.5), ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    option1Text = visual.TextStim(win=win, name='option1Text',
        text='',
        font='Open Sans',
        pos=((-win.size[0]/3), -300), height=40.0, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    option1Image = visual.ImageStim(
        win=win,
        name='option1Image', 
        image='default.png', mask=None, anchor='center',
        ori=0.0, pos=((-win.size[0]/3), 0), size=(win.size[0]/5,None),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-2.0)
    option2Text = visual.TextStim(win=win, name='option2Text',
        text='',
        font='Open Sans',
        pos=(0, -300), height=40.0, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-3.0);
    option2Image = visual.ImageStim(
        win=win,
        name='option2Image', 
        image='default.png', mask=None, anchor='center',
        ori=0.0, pos=(0.0,0.0), size=(win.size[0]/5,None),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-4.0)
    option3Text = visual.TextStim(win=win, name='option3Text',
        text='',
        font='Open Sans',
        pos=(win.size[0]/3, -300), height=40.0, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-5.0);
    option3Image = visual.ImageStim(
        win=win,
        name='option3Image', 
        image='default.png', mask=None, anchor='center',
        ori=0.0, pos=(win.size[0]/3, 0), size=(win.size[0]/5,None),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-6.0)
    mouse = event.Mouse(win=win)
    x, y = [None, None]
    mouse.mouseClock = core.Clock()
    
    # --- Initialize components for Routine "baseline" ---
    mouse_4 = event.Mouse(win=win)
    x, y = [None, None]
    mouse_4.mouseClock = core.Clock()
    movie = visual.MovieStim(
        win, name='movie',
        filename='baselineVideo.mkv', movieLib='ffpyplayer',
        loop=False, volume=1.0, noAudio=False,
        pos=(0, 0), size=(1920,1080), units=win.units,
        ori=0.0, anchor='center',opacity=None, contrast=1.0,
        depth=-1
    )
    cortex_rec = visual.BaseVisualStim(win=win, name="cortex_rec")
    cortex_obj = emotiv.Cortex(subject=expInfo['participant'])
    
    # --- Initialize components for Routine "clicktoContinue" ---
    text_click_to_continue = visual.TextStim(win=win, name='text_click_to_continue',
        text='Click anywhere to continue',
        font='Open Sans',
        pos=(0, 0), height=60.0, wrapWidth=1500.0, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    mouse_5 = event.Mouse(win=win)
    x, y = [None, None]
    mouse_5.mouseClock = core.Clock()
    
    # --- Initialize components for Routine "countDown" ---
    Three = visual.TextStim(win=win, name='Three',
        text='3',
        font='Open Sans',
        pos=(0, 0), height=180.0, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    Two = visual.TextStim(win=win, name='Two',
        text='2',
        font='Open Sans',
        pos=(0, 0), height=180.0, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    One = visual.TextStim(win=win, name='One',
        text='1',
        font='Open Sans',
        pos=(0, 0), height=180.0, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    
    # --- Initialize components for Routine "playClip" ---
    stimclip = visual.MovieStim(
        win, name='stimclip',
        filename=None, movieLib='ffpyplayer',
        loop=False, volume=1.0, noAudio=False,
        pos=(0, 0), size=(1.0, 1.0), units='pix',
        ori=0.0, anchor='center',opacity=None, contrast=1.0,
        depth=0
    )
    mouse_2 = event.Mouse(win=win)
    x, y = [None, None]
    mouse_2.mouseClock = core.Clock()
    # This is generated by writeInitCode
    eeg_marker_stim_video = visual.BaseVisualStim(win=win, name="eeg_marker_stim_video")
    
    # --- Initialize components for Routine "positiveNegative" ---
    # Run 'Begin Experiment' code from code_2
    # Code inserted in positivenegative, begin experiment section
    agree = visual.Slider(win=win, name='agree',
        startValue=None, size=(win.size[0]-250,50), pos=(0, -100), units=win.units,
        labels=('Strongly Disagree','disagree','Neutral','Agree','Strongly Agree'), ticks=(1, 2, 3, 4, 5), granularity=1.0,
        style='rating', styleTweaks=(), opacity=None,
        labelColor='LightGray', markerColor='Red', lineColor='White', colorSpace='rgb',
        font='Open Sans', labelHeight=25.0,
        flip=False, ori=0.0, depth=-1, readOnly=False)
    text = visual.TextStim(win=win, name='text',
        text='',
        font='Open Sans',
        pos=(0, 300), height=60.0, wrapWidth=(win.size[0]-200), ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    # This is generated by writeInitCode
    eeg_marker_rating = visual.BaseVisualStim(win=win, name="eeg_marker_rating")
    
    # --- Initialize components for Routine "countDown" ---
    Three = visual.TextStim(win=win, name='Three',
        text='3',
        font='Open Sans',
        pos=(0, 0), height=180.0, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    Two = visual.TextStim(win=win, name='Two',
        text='2',
        font='Open Sans',
        pos=(0, 0), height=180.0, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    One = visual.TextStim(win=win, name='One',
        text='1',
        font='Open Sans',
        pos=(0, 0), height=180.0, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    
    # --- Initialize components for Routine "neutralVideo" ---
    neutralVideoClip = visual.MovieStim(
        win, name='neutralVideoClip',
        filename=None, movieLib='ffpyplayer',
        loop=False, volume=1.0, noAudio=False,
        pos=(0, 0), size=(1.0, 1.0), units=win.units,
        ori=0.0, anchor='center',opacity=None, contrast=1.0,
        depth=0
    )
    mouse_3 = event.Mouse(win=win)
    x, y = [None, None]
    mouse_3.mouseClock = core.Clock()
    # This is generated by writeInitCode
    eeg_marker_neutral_video = visual.BaseVisualStim(win=win, name="eeg_marker_neutral_video")
    
    # create some handy timers
    if globalClock is None:
        globalClock = core.Clock()  # to track the time since experiment started
    if ioServer is not None:
        ioServer.syncClock(globalClock)
    logging.setDefaultClock(globalClock)
    routineTimer = core.Clock()  # to track time remaining of each (possibly non-slip) routine
    win.flip()  # flip window to reset last flip timer
    # store the exact time the global clock started
    expInfo['expStart'] = data.getDateStr(format='%Y-%m-%d %Hh%M.%S.%f %z', fractionalSecondDigits=6)
    
    # set up handler to look after randomisation of conditions etc
    chooseCategoriesLoop = data.TrialHandler(nReps=1.0, method='sequential', 
        extraInfo=expInfo, originPath=-1,
        trialList=selectionTrialsList,
        seed=None, name='chooseCategoriesLoop')
    thisExp.addLoop(chooseCategoriesLoop)  # add the loop to the experiment
    thisChooseCategoriesLoop = chooseCategoriesLoop.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisChooseCategoriesLoop.rgb)
    if thisChooseCategoriesLoop != None:
        for paramName in thisChooseCategoriesLoop:
            globals()[paramName] = thisChooseCategoriesLoop[paramName]
    
    for thisChooseCategoriesLoop in chooseCategoriesLoop:
        currentLoop = chooseCategoriesLoop
        thisExp.timestampOnFlip(win, 'thisRow.t')
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                inputs=inputs, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
        )
        # abbreviate parameter names if possible (e.g. rgb = thisChooseCategoriesLoop.rgb)
        if thisChooseCategoriesLoop != None:
            for paramName in thisChooseCategoriesLoop:
                globals()[paramName] = thisChooseCategoriesLoop[paramName]
        
        # --- Prepare to start Routine "chooseCategoriesTrial" ---
        continueRoutine = True
        # update component parameters for each repeat
        thisExp.addData('chooseCategoriesTrial.started', globalClock.getTime())
        option1Text.setText(text1)
        option1Image.setImage(image1)
        option2Text.setText(text2)
        option2Image.setImage(image2)
        option3Text.setText(text3)
        option3Image.setImage(image3)
        # setup some python lists for storing info about the mouse
        mouse.x = []
        mouse.y = []
        mouse.leftButton = []
        mouse.midButton = []
        mouse.rightButton = []
        mouse.time = []
        mouse.clicked_name = []
        gotValidClick = False  # until a click is received
        # keep track of which components have finished
        chooseCategoriesTrialComponents = [instructions, option1Text, option1Image, option2Text, option2Image, option3Text, option3Image, mouse]
        for thisComponent in chooseCategoriesTrialComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "chooseCategoriesTrial" ---
        routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *instructions* updates
            
            # if instructions is starting this frame...
            if instructions.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                instructions.frameNStart = frameN  # exact frame index
                instructions.tStart = t  # local t and not account for scr refresh
                instructions.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(instructions, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'instructions.started')
                # update status
                instructions.status = STARTED
                instructions.setAutoDraw(True)
            
            # if instructions is active this frame...
            if instructions.status == STARTED:
                # update params
                pass
            
            # *option1Text* updates
            
            # if option1Text is starting this frame...
            if option1Text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                option1Text.frameNStart = frameN  # exact frame index
                option1Text.tStart = t  # local t and not account for scr refresh
                option1Text.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(option1Text, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'option1Text.started')
                # update status
                option1Text.status = STARTED
                option1Text.setAutoDraw(True)
            
            # if option1Text is active this frame...
            if option1Text.status == STARTED:
                # update params
                pass
            
            # *option1Image* updates
            
            # if option1Image is starting this frame...
            if option1Image.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                option1Image.frameNStart = frameN  # exact frame index
                option1Image.tStart = t  # local t and not account for scr refresh
                option1Image.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(option1Image, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'option1Image.started')
                # update status
                option1Image.status = STARTED
                option1Image.setAutoDraw(True)
            
            # if option1Image is active this frame...
            if option1Image.status == STARTED:
                # update params
                pass
            
            # *option2Text* updates
            
            # if option2Text is starting this frame...
            if option2Text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                option2Text.frameNStart = frameN  # exact frame index
                option2Text.tStart = t  # local t and not account for scr refresh
                option2Text.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(option2Text, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'option2Text.started')
                # update status
                option2Text.status = STARTED
                option2Text.setAutoDraw(True)
            
            # if option2Text is active this frame...
            if option2Text.status == STARTED:
                # update params
                pass
            
            # *option2Image* updates
            
            # if option2Image is starting this frame...
            if option2Image.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                option2Image.frameNStart = frameN  # exact frame index
                option2Image.tStart = t  # local t and not account for scr refresh
                option2Image.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(option2Image, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'option2Image.started')
                # update status
                option2Image.status = STARTED
                option2Image.setAutoDraw(True)
            
            # if option2Image is active this frame...
            if option2Image.status == STARTED:
                # update params
                pass
            
            # *option3Text* updates
            
            # if option3Text is starting this frame...
            if option3Text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                option3Text.frameNStart = frameN  # exact frame index
                option3Text.tStart = t  # local t and not account for scr refresh
                option3Text.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(option3Text, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'option3Text.started')
                # update status
                option3Text.status = STARTED
                option3Text.setAutoDraw(True)
            
            # if option3Text is active this frame...
            if option3Text.status == STARTED:
                # update params
                pass
            
            # *option3Image* updates
            
            # if option3Image is starting this frame...
            if option3Image.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                option3Image.frameNStart = frameN  # exact frame index
                option3Image.tStart = t  # local t and not account for scr refresh
                option3Image.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(option3Image, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'option3Image.started')
                # update status
                option3Image.status = STARTED
                option3Image.setAutoDraw(True)
            
            # if option3Image is active this frame...
            if option3Image.status == STARTED:
                # update params
                pass
            # *mouse* updates
            
            # if mouse is starting this frame...
            if mouse.status == NOT_STARTED and t >= 0.2-frameTolerance:
                # keep track of start time/frame for later
                mouse.frameNStart = frameN  # exact frame index
                mouse.tStart = t  # local t and not account for scr refresh
                mouse.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(mouse, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.addData('mouse.started', t)
                # update status
                mouse.status = STARTED
                mouse.mouseClock.reset()
                prevButtonState = mouse.getPressed()  # if button is down already this ISN'T a new click
            if mouse.status == STARTED:  # only update if started and not finished!
                buttons = mouse.getPressed()
                if buttons != prevButtonState:  # button state changed?
                    prevButtonState = buttons
                    if sum(buttons) > 0:  # state changed to a new click
                        # check if the mouse was inside our 'clickable' objects
                        gotValidClick = False
                        clickableList = environmenttools.getFromNames([option1Image, option1Text,option2Image, option2Text, option3Image, option3Text], namespace=locals())
                        for obj in clickableList:
                            # is this object clicked on?
                            if obj.contains(mouse):
                                gotValidClick = True
                                mouse.clicked_name.append(obj.name)
                        if gotValidClick:
                            x, y = mouse.getPos()
                            mouse.x.append(x)
                            mouse.y.append(y)
                            buttons = mouse.getPressed()
                            mouse.leftButton.append(buttons[0])
                            mouse.midButton.append(buttons[1])
                            mouse.rightButton.append(buttons[2])
                            mouse.time.append(mouse.mouseClock.getTime())
                        if gotValidClick:
                            continueRoutine = False  # end routine on response
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, inputs=inputs, win=win)
                return
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in chooseCategoriesTrialComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "chooseCategoriesTrial" ---
        for thisComponent in chooseCategoriesTrialComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        thisExp.addData('chooseCategoriesTrial.stopped', globalClock.getTime())
        # store data for chooseCategoriesLoop (TrialHandler)
        chooseCategoriesLoop.addData('mouse.x', mouse.x)
        chooseCategoriesLoop.addData('mouse.y', mouse.y)
        chooseCategoriesLoop.addData('mouse.leftButton', mouse.leftButton)
        chooseCategoriesLoop.addData('mouse.midButton', mouse.midButton)
        chooseCategoriesLoop.addData('mouse.rightButton', mouse.rightButton)
        chooseCategoriesLoop.addData('mouse.time', mouse.time)
        chooseCategoriesLoop.addData('mouse.clicked_name', mouse.clicked_name)
        # Run 'End Routine' code from code
        if mouse.clicked_name == ['option1Image'] or mouse.clicked_name == ['option1Text']: #TODO: come here and add all options
            print('Clicked 1 dummy')
            experimentTrialsList[mainIndex]['stim']= stimuli1
        
        elif mouse.clicked_name == ['option2Image'] or mouse.clicked_name == ['option2Text']: #TODO: come here and add all options
            print('Clicked 2 dummy')
            experimentTrialsList[mainIndex]['stim']= stimuli2
        
        elif mouse.clicked_name == ['option3Image'] or mouse.clicked_name == ['option3Text']: #TODO: come here and add all options
            print('Clicked 3 dummy')
            experimentTrialsList[mainIndex]['stim']= stimuli3
        print('stim video file',experimentTrialsList[mainIndex]['stim'])
        # the Routine "chooseCategoriesTrial" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
    # completed 1.0 repeats of 'chooseCategoriesLoop'
    
    
    # --- Prepare to start Routine "baseline" ---
    continueRoutine = True
    # update component parameters for each repeat
    thisExp.addData('baseline.started', globalClock.getTime())
    # setup some python lists for storing info about the mouse_4
    mouse_4.x = []
    mouse_4.y = []
    mouse_4.leftButton = []
    mouse_4.midButton = []
    mouse_4.rightButton = []
    mouse_4.time = []
    gotValidClick = False  # until a click is received
    # keep track of which components have finished
    baselineComponents = [mouse_4, movie, cortex_rec]
    for thisComponent in baselineComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "baseline" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # *mouse_4* updates
        
        # if mouse_4 is starting this frame...
        if mouse_4.status == NOT_STARTED and t >= 1-frameTolerance:
            # keep track of start time/frame for later
            mouse_4.frameNStart = frameN  # exact frame index
            mouse_4.tStart = t  # local t and not account for scr refresh
            mouse_4.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(mouse_4, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.addData('mouse_4.started', t)
            # update status
            mouse_4.status = STARTED
            mouse_4.mouseClock.reset()
            prevButtonState = mouse_4.getPressed()  # if button is down already this ISN'T a new click
        if mouse_4.status == STARTED:  # only update if started and not finished!
            buttons = mouse_4.getPressed()
            if buttons != prevButtonState:  # button state changed?
                prevButtonState = buttons
                if sum(buttons) > 0:  # state changed to a new click
                    x, y = mouse_4.getPos()
                    mouse_4.x.append(x)
                    mouse_4.y.append(y)
                    buttons = mouse_4.getPressed()
                    mouse_4.leftButton.append(buttons[0])
                    mouse_4.midButton.append(buttons[1])
                    mouse_4.rightButton.append(buttons[2])
                    mouse_4.time.append(mouse_4.mouseClock.getTime())
                    
                    continueRoutine = False  # end routine on response
        
        # *movie* updates
        
        # if movie is starting this frame...
        if movie.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            movie.frameNStart = frameN  # exact frame index
            movie.tStart = t  # local t and not account for scr refresh
            movie.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(movie, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'movie.started')
            # update status
            movie.status = STARTED
            movie.setAutoDraw(True)
            movie.play()
        if movie.isFinished:  # force-end the Routine
            continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, inputs=inputs, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in baselineComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "baseline" ---
    for thisComponent in baselineComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.addData('baseline.stopped', globalClock.getTime())
    # store data for thisExp (ExperimentHandler)
    thisExp.addData('mouse_4.x', mouse_4.x)
    thisExp.addData('mouse_4.y', mouse_4.y)
    thisExp.addData('mouse_4.leftButton', mouse_4.leftButton)
    thisExp.addData('mouse_4.midButton', mouse_4.midButton)
    thisExp.addData('mouse_4.rightButton', mouse_4.rightButton)
    thisExp.addData('mouse_4.time', mouse_4.time)
    thisExp.nextEntry()
    movie.stop()  # ensure movie has stopped at end of Routine
    # the Routine "baseline" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "clicktoContinue" ---
    continueRoutine = True
    # update component parameters for each repeat
    thisExp.addData('clicktoContinue.started', globalClock.getTime())
    # setup some python lists for storing info about the mouse_5
    mouse_5.x = []
    mouse_5.y = []
    mouse_5.leftButton = []
    mouse_5.midButton = []
    mouse_5.rightButton = []
    mouse_5.time = []
    gotValidClick = False  # until a click is received
    # keep track of which components have finished
    clicktoContinueComponents = [text_click_to_continue, mouse_5]
    for thisComponent in clicktoContinueComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "clicktoContinue" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *text_click_to_continue* updates
        
        # if text_click_to_continue is starting this frame...
        if text_click_to_continue.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            text_click_to_continue.frameNStart = frameN  # exact frame index
            text_click_to_continue.tStart = t  # local t and not account for scr refresh
            text_click_to_continue.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_click_to_continue, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text_click_to_continue.started')
            # update status
            text_click_to_continue.status = STARTED
            text_click_to_continue.setAutoDraw(True)
        
        # if text_click_to_continue is active this frame...
        if text_click_to_continue.status == STARTED:
            # update params
            pass
        # *mouse_5* updates
        
        # if mouse_5 is starting this frame...
        if mouse_5.status == NOT_STARTED and t >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            mouse_5.frameNStart = frameN  # exact frame index
            mouse_5.tStart = t  # local t and not account for scr refresh
            mouse_5.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(mouse_5, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.addData('mouse_5.started', t)
            # update status
            mouse_5.status = STARTED
            mouse_5.mouseClock.reset()
            prevButtonState = mouse_5.getPressed()  # if button is down already this ISN'T a new click
        if mouse_5.status == STARTED:  # only update if started and not finished!
            buttons = mouse_5.getPressed()
            if buttons != prevButtonState:  # button state changed?
                prevButtonState = buttons
                if sum(buttons) > 0:  # state changed to a new click
                    x, y = mouse_5.getPos()
                    mouse_5.x.append(x)
                    mouse_5.y.append(y)
                    buttons = mouse_5.getPressed()
                    mouse_5.leftButton.append(buttons[0])
                    mouse_5.midButton.append(buttons[1])
                    mouse_5.rightButton.append(buttons[2])
                    mouse_5.time.append(mouse_5.mouseClock.getTime())
                    
                    continueRoutine = False  # end routine on response
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, inputs=inputs, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in clicktoContinueComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "clicktoContinue" ---
    for thisComponent in clicktoContinueComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.addData('clicktoContinue.stopped', globalClock.getTime())
    # store data for thisExp (ExperimentHandler)
    thisExp.addData('mouse_5.x', mouse_5.x)
    thisExp.addData('mouse_5.y', mouse_5.y)
    thisExp.addData('mouse_5.leftButton', mouse_5.leftButton)
    thisExp.addData('mouse_5.midButton', mouse_5.midButton)
    thisExp.addData('mouse_5.rightButton', mouse_5.rightButton)
    thisExp.addData('mouse_5.time', mouse_5.time)
    thisExp.nextEntry()
    # the Routine "clicktoContinue" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    trials = data.TrialHandler(nReps=1.0, method='sequential', 
        extraInfo=expInfo, originPath=-1,
        trialList=experimentTrialsList,
        seed=None, name='trials')
    thisExp.addLoop(trials)  # add the loop to the experiment
    thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial:
            globals()[paramName] = thisTrial[paramName]
    
    for thisTrial in trials:
        currentLoop = trials
        thisExp.timestampOnFlip(win, 'thisRow.t')
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                inputs=inputs, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
        )
        # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
        if thisTrial != None:
            for paramName in thisTrial:
                globals()[paramName] = thisTrial[paramName]
        
        # --- Prepare to start Routine "countDown" ---
        continueRoutine = True
        # update component parameters for each repeat
        thisExp.addData('countDown.started', globalClock.getTime())
        # keep track of which components have finished
        countDownComponents = [Three, Two, One]
        for thisComponent in countDownComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "countDown" ---
        routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 3.0:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *Three* updates
            
            # if Three is starting this frame...
            if Three.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                Three.frameNStart = frameN  # exact frame index
                Three.tStart = t  # local t and not account for scr refresh
                Three.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Three, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'Three.started')
                # update status
                Three.status = STARTED
                Three.setAutoDraw(True)
            
            # if Three is active this frame...
            if Three.status == STARTED:
                # update params
                pass
            
            # if Three is stopping this frame...
            if Three.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > Three.tStartRefresh + 1.0-frameTolerance:
                    # keep track of stop time/frame for later
                    Three.tStop = t  # not accounting for scr refresh
                    Three.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'Three.stopped')
                    # update status
                    Three.status = FINISHED
                    Three.setAutoDraw(False)
            
            # *Two* updates
            
            # if Two is starting this frame...
            if Two.status == NOT_STARTED and tThisFlip >= 1-frameTolerance:
                # keep track of start time/frame for later
                Two.frameNStart = frameN  # exact frame index
                Two.tStart = t  # local t and not account for scr refresh
                Two.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Two, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'Two.started')
                # update status
                Two.status = STARTED
                Two.setAutoDraw(True)
            
            # if Two is active this frame...
            if Two.status == STARTED:
                # update params
                pass
            
            # if Two is stopping this frame...
            if Two.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > Two.tStartRefresh + 1.0-frameTolerance:
                    # keep track of stop time/frame for later
                    Two.tStop = t  # not accounting for scr refresh
                    Two.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'Two.stopped')
                    # update status
                    Two.status = FINISHED
                    Two.setAutoDraw(False)
            
            # *One* updates
            
            # if One is starting this frame...
            if One.status == NOT_STARTED and tThisFlip >= 2-frameTolerance:
                # keep track of start time/frame for later
                One.frameNStart = frameN  # exact frame index
                One.tStart = t  # local t and not account for scr refresh
                One.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(One, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'One.started')
                # update status
                One.status = STARTED
                One.setAutoDraw(True)
            
            # if One is active this frame...
            if One.status == STARTED:
                # update params
                pass
            
            # if One is stopping this frame...
            if One.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > One.tStartRefresh + 1.0-frameTolerance:
                    # keep track of stop time/frame for later
                    One.tStop = t  # not accounting for scr refresh
                    One.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'One.stopped')
                    # update status
                    One.status = FINISHED
                    One.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, inputs=inputs, win=win)
                return
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in countDownComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "countDown" ---
        for thisComponent in countDownComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        thisExp.addData('countDown.stopped', globalClock.getTime())
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if routineForceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-3.000000)
        
        # --- Prepare to start Routine "playClip" ---
        continueRoutine = True
        # update component parameters for each repeat
        thisExp.addData('playClip.started', globalClock.getTime())
        stimclip.setMovie(stim)
        # Run 'Begin Routine' code from code_3
        try:
            window_width, window_height = win.size
            print('stim clip size:', stimclip.size)
            print('stim clip original size:', stimclip.frameSize)
            
            # Get the original size of the video
            orig_width, orig_height = stimclip.frameSize
            
            # Calculate the scaling factors for width and height
            scale_width = window_width / orig_width
            scale_height = window_height / orig_height
            
            # Use the smaller scaling factor to maintain aspect ratio
            scale_factor = min(scale_width, scale_height)
            
            # Scale the size of the stimclip proportionally
            new_width = int(orig_width * scale_factor)
            new_height = int(orig_height * scale_factor)
            
            # Set the size of the stimclip to maintain aspect ratio
            stimclip.size = (new_width, new_height)
        except Exception as e:
            print('Exception:', e)
            # Handle the exception if necessary
            # stimclip.size=1000,1000#stimclip.size=stimclip.origSize()
        # setup some python lists for storing info about the mouse_2
        mouse_2.x = []
        mouse_2.y = []
        mouse_2.leftButton = []
        mouse_2.midButton = []
        mouse_2.rightButton = []
        mouse_2.time = []
        gotValidClick = False  # until a click is received
        # This is generated by the writeRoutineStartCode
        # keep track of which components have finished
        playClipComponents = [stimclip, mouse_2, eeg_marker_stim_video]
        for thisComponent in playClipComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "playClip" ---
        routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *stimclip* updates
            
            # if stimclip is starting this frame...
            if stimclip.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                stimclip.frameNStart = frameN  # exact frame index
                stimclip.tStart = t  # local t and not account for scr refresh
                stimclip.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(stimclip, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'stimclip.started')
                # update status
                stimclip.status = STARTED
                stimclip.setAutoDraw(True)
                stimclip.play()
            if stimclip.isFinished:  # force-end the Routine
                continueRoutine = False
            # *mouse_2* updates
            
            # if mouse_2 is starting this frame...
            if mouse_2.status == NOT_STARTED and t >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                mouse_2.frameNStart = frameN  # exact frame index
                mouse_2.tStart = t  # local t and not account for scr refresh
                mouse_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(mouse_2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.addData('mouse_2.started', t)
                # update status
                mouse_2.status = STARTED
                mouse_2.mouseClock.reset()
                prevButtonState = mouse_2.getPressed()  # if button is down already this ISN'T a new click
            if mouse_2.status == STARTED:  # only update if started and not finished!
                buttons = mouse_2.getPressed()
                if buttons != prevButtonState:  # button state changed?
                    prevButtonState = buttons
                    if sum(buttons) > 0:  # state changed to a new click
                        x, y = mouse_2.getPos()
                        mouse_2.x.append(x)
                        mouse_2.y.append(y)
                        buttons = mouse_2.getPressed()
                        mouse_2.leftButton.append(buttons[0])
                        mouse_2.midButton.append(buttons[1])
                        mouse_2.rightButton.append(buttons[2])
                        mouse_2.time.append(mouse_2.mouseClock.getTime())
                        
                        continueRoutine = False  # end routine on response
            
            # if eeg_marker_stim_video is starting this frame...
            if eeg_marker_stim_video.status == NOT_STARTED and t >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                eeg_marker_stim_video.frameNStart = frameN  # exact frame index
                eeg_marker_stim_video.tStart = t  # local t and not account for scr refresh
                eeg_marker_stim_video.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(eeg_marker_stim_video, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.addData('eeg_marker_stim_video.started', t)
                # update status
                eeg_marker_stim_video.status = STARTED
                eeg_marker_stim_video.status = STARTED
                delta_time = tThisFlip-t  # Adding the extra time between now and the next screen flip
                cortex_obj.inject_marker(value=str('1'), label=stim, delta_time=delta_time)
                eeg_marker_stim_video.start_sent = True
            
            # if eeg_marker_stim_video is stopping this frame...
            if eeg_marker_stim_video.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > eeg_marker_stim_video.tStartRefresh + 1-frameTolerance:
                    # keep track of stop time/frame for later
                    eeg_marker_stim_video.tStop = t  # not accounting for scr refresh
                    eeg_marker_stim_video.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.addData('eeg_marker_stim_video.stopped', t)
                    # update status
                    eeg_marker_stim_video.status = FINISHED
                    eeg_marker_stim_video.status = FINISHED
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, inputs=inputs, win=win)
                return
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in playClipComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "playClip" ---
        for thisComponent in playClipComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        thisExp.addData('playClip.stopped', globalClock.getTime())
        stimclip.stop()  # ensure movie has stopped at end of Routine
        # store data for trials (TrialHandler)
        trials.addData('mouse_2.x', mouse_2.x)
        trials.addData('mouse_2.y', mouse_2.y)
        trials.addData('mouse_2.leftButton', mouse_2.leftButton)
        trials.addData('mouse_2.midButton', mouse_2.midButton)
        trials.addData('mouse_2.rightButton', mouse_2.rightButton)
        trials.addData('mouse_2.time', mouse_2.time)
        # This is generated by the writeRoutineEndCode
        # the Routine "playClip" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "positiveNegative" ---
        continueRoutine = True
        # update component parameters for each repeat
        thisExp.addData('positiveNegative.started', globalClock.getTime())
        agree.reset()
        text.setText('I feel '+ emotion)
        # This is generated by the writeRoutineStartCode
        # keep track of which components have finished
        positiveNegativeComponents = [agree, text, eeg_marker_rating]
        for thisComponent in positiveNegativeComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "positiveNegative" ---
        routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            # Run 'Each Frame' code from code_2
            # Code inserted in positivenegative, each frame section
            
            # *agree* updates
            
            # if agree is starting this frame...
            if agree.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                agree.frameNStart = frameN  # exact frame index
                agree.tStart = t  # local t and not account for scr refresh
                agree.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(agree, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'agree.started')
                # update status
                agree.status = STARTED
                agree.setAutoDraw(True)
            
            # if agree is active this frame...
            if agree.status == STARTED:
                # update params
                pass
            
            # Check agree for response to end Routine
            if agree.getRating() is not None and agree.status == STARTED:
                continueRoutine = False
            
            # *text* updates
            
            # if text is starting this frame...
            if text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                text.frameNStart = frameN  # exact frame index
                text.tStart = t  # local t and not account for scr refresh
                text.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(text, 'tStartRefresh')  # time at next scr refresh
                # update status
                text.status = STARTED
                text.setAutoDraw(True)
            
            # if text is active this frame...
            if text.status == STARTED:
                # update params
                pass
            
            # if eeg_marker_rating is starting this frame...
            if eeg_marker_rating.status == NOT_STARTED and t >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                eeg_marker_rating.frameNStart = frameN  # exact frame index
                eeg_marker_rating.tStart = t  # local t and not account for scr refresh
                eeg_marker_rating.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(eeg_marker_rating, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.addData('eeg_marker_rating.started', t)
                # update status
                eeg_marker_rating.status = STARTED
                eeg_marker_rating.status = STARTED
                delta_time = tThisFlip-t  # Adding the extra time between now and the next screen flip
                cortex_obj.inject_marker(value=str('1'), label='label', delta_time=delta_time)
                eeg_marker_rating.start_sent = True
            
            # if eeg_marker_rating is stopping this frame...
            if eeg_marker_rating.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > eeg_marker_rating.tStartRefresh + 1-frameTolerance:
                    # keep track of stop time/frame for later
                    eeg_marker_rating.tStop = t  # not accounting for scr refresh
                    eeg_marker_rating.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.addData('eeg_marker_rating.stopped', t)
                    # update status
                    eeg_marker_rating.status = FINISHED
                    eeg_marker_rating.status = FINISHED
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, inputs=inputs, win=win)
                return
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in positiveNegativeComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "positiveNegative" ---
        for thisComponent in positiveNegativeComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        thisExp.addData('positiveNegative.stopped', globalClock.getTime())
        trials.addData('agree.response', agree.getRating())
        trials.addData('agree.rt', agree.getRT())
        # This is generated by the writeRoutineEndCode
        # the Routine "positiveNegative" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "countDown" ---
        continueRoutine = True
        # update component parameters for each repeat
        thisExp.addData('countDown.started', globalClock.getTime())
        # keep track of which components have finished
        countDownComponents = [Three, Two, One]
        for thisComponent in countDownComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "countDown" ---
        routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 3.0:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *Three* updates
            
            # if Three is starting this frame...
            if Three.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                Three.frameNStart = frameN  # exact frame index
                Three.tStart = t  # local t and not account for scr refresh
                Three.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Three, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'Three.started')
                # update status
                Three.status = STARTED
                Three.setAutoDraw(True)
            
            # if Three is active this frame...
            if Three.status == STARTED:
                # update params
                pass
            
            # if Three is stopping this frame...
            if Three.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > Three.tStartRefresh + 1.0-frameTolerance:
                    # keep track of stop time/frame for later
                    Three.tStop = t  # not accounting for scr refresh
                    Three.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'Three.stopped')
                    # update status
                    Three.status = FINISHED
                    Three.setAutoDraw(False)
            
            # *Two* updates
            
            # if Two is starting this frame...
            if Two.status == NOT_STARTED and tThisFlip >= 1-frameTolerance:
                # keep track of start time/frame for later
                Two.frameNStart = frameN  # exact frame index
                Two.tStart = t  # local t and not account for scr refresh
                Two.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Two, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'Two.started')
                # update status
                Two.status = STARTED
                Two.setAutoDraw(True)
            
            # if Two is active this frame...
            if Two.status == STARTED:
                # update params
                pass
            
            # if Two is stopping this frame...
            if Two.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > Two.tStartRefresh + 1.0-frameTolerance:
                    # keep track of stop time/frame for later
                    Two.tStop = t  # not accounting for scr refresh
                    Two.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'Two.stopped')
                    # update status
                    Two.status = FINISHED
                    Two.setAutoDraw(False)
            
            # *One* updates
            
            # if One is starting this frame...
            if One.status == NOT_STARTED and tThisFlip >= 2-frameTolerance:
                # keep track of start time/frame for later
                One.frameNStart = frameN  # exact frame index
                One.tStart = t  # local t and not account for scr refresh
                One.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(One, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'One.started')
                # update status
                One.status = STARTED
                One.setAutoDraw(True)
            
            # if One is active this frame...
            if One.status == STARTED:
                # update params
                pass
            
            # if One is stopping this frame...
            if One.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > One.tStartRefresh + 1.0-frameTolerance:
                    # keep track of stop time/frame for later
                    One.tStop = t  # not accounting for scr refresh
                    One.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'One.stopped')
                    # update status
                    One.status = FINISHED
                    One.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, inputs=inputs, win=win)
                return
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in countDownComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "countDown" ---
        for thisComponent in countDownComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        thisExp.addData('countDown.stopped', globalClock.getTime())
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if routineForceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-3.000000)
        
        # --- Prepare to start Routine "neutralVideo" ---
        continueRoutine = True
        # update component parameters for each repeat
        thisExp.addData('neutralVideo.started', globalClock.getTime())
        neutralVideoClip.setMovie(neutralvideo)
        # setup some python lists for storing info about the mouse_3
        mouse_3.x = []
        mouse_3.y = []
        mouse_3.leftButton = []
        mouse_3.midButton = []
        mouse_3.rightButton = []
        mouse_3.time = []
        gotValidClick = False  # until a click is received
        # Run 'Begin Routine' code from code_5
        try:
            window_width, window_height = win.size
            print('stim clip size:', neutralVideoClip.size)
            print('stim clip original size:', neutralVideoClip.frameSize)
            
            # Get the original size of the video
            orig_width, orig_height = neutralVideoClip.frameSize
            
            # Calculate the scaling factors for width and height
            scale_width = window_width / orig_width
            scale_height = window_height / orig_height
            
            # Use the smaller scaling factor to maintain aspect ratio
            scale_factor = min(scale_width, scale_height)
            
            # Scale the size of the neutralVideoClip proportionally
            new_width = int(orig_width * scale_factor)
            new_height = int(orig_height * scale_factor)
            
            # Set the size of the neutralVideoClip to maintain aspect ratio
            neutralVideoClip.size = (new_width, new_height)
        except Exception as e:
            print('Exception:', e)
            # Handle the exception if necessary
            # neutralVideoClip.size=1000,1000#neutralVideoClip.size=neuneutralVideoClip.origSize()
        # This is generated by the writeRoutineStartCode
        # keep track of which components have finished
        neutralVideoComponents = [neutralVideoClip, mouse_3, eeg_marker_neutral_video]
        for thisComponent in neutralVideoComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "neutralVideo" ---
        routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *neutralVideoClip* updates
            
            # if neutralVideoClip is starting this frame...
            if neutralVideoClip.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                neutralVideoClip.frameNStart = frameN  # exact frame index
                neutralVideoClip.tStart = t  # local t and not account for scr refresh
                neutralVideoClip.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(neutralVideoClip, 'tStartRefresh')  # time at next scr refresh
                # update status
                neutralVideoClip.status = STARTED
                neutralVideoClip.setAutoDraw(True)
                neutralVideoClip.play()
            if neutralVideoClip.isFinished:  # force-end the Routine
                continueRoutine = False
            # *mouse_3* updates
            
            # if mouse_3 is starting this frame...
            if mouse_3.status == NOT_STARTED and t >= .2-frameTolerance:
                # keep track of start time/frame for later
                mouse_3.frameNStart = frameN  # exact frame index
                mouse_3.tStart = t  # local t and not account for scr refresh
                mouse_3.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(mouse_3, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.addData('mouse_3.started', t)
                # update status
                mouse_3.status = STARTED
                mouse_3.mouseClock.reset()
                prevButtonState = mouse_3.getPressed()  # if button is down already this ISN'T a new click
            if mouse_3.status == STARTED:  # only update if started and not finished!
                buttons = mouse_3.getPressed()
                if buttons != prevButtonState:  # button state changed?
                    prevButtonState = buttons
                    if sum(buttons) > 0:  # state changed to a new click
                        x, y = mouse_3.getPos()
                        mouse_3.x.append(x)
                        mouse_3.y.append(y)
                        buttons = mouse_3.getPressed()
                        mouse_3.leftButton.append(buttons[0])
                        mouse_3.midButton.append(buttons[1])
                        mouse_3.rightButton.append(buttons[2])
                        mouse_3.time.append(mouse_3.mouseClock.getTime())
                        
                        continueRoutine = False  # end routine on response
            
            # if eeg_marker_neutral_video is starting this frame...
            if eeg_marker_neutral_video.status == NOT_STARTED and t >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                eeg_marker_neutral_video.frameNStart = frameN  # exact frame index
                eeg_marker_neutral_video.tStart = t  # local t and not account for scr refresh
                eeg_marker_neutral_video.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(eeg_marker_neutral_video, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.addData('eeg_marker_neutral_video.started', t)
                # update status
                eeg_marker_neutral_video.status = STARTED
                eeg_marker_neutral_video.status = STARTED
                delta_time = tThisFlip-t  # Adding the extra time between now and the next screen flip
                cortex_obj.inject_marker(value=str('1'), label='label', delta_time=delta_time)
                eeg_marker_neutral_video.start_sent = True
            
            # if eeg_marker_neutral_video is stopping this frame...
            if eeg_marker_neutral_video.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > eeg_marker_neutral_video.tStartRefresh + 1-frameTolerance:
                    # keep track of stop time/frame for later
                    eeg_marker_neutral_video.tStop = t  # not accounting for scr refresh
                    eeg_marker_neutral_video.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.addData('eeg_marker_neutral_video.stopped', t)
                    # update status
                    eeg_marker_neutral_video.status = FINISHED
                    eeg_marker_neutral_video.status = FINISHED
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, inputs=inputs, win=win)
                return
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in neutralVideoComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "neutralVideo" ---
        for thisComponent in neutralVideoComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        thisExp.addData('neutralVideo.stopped', globalClock.getTime())
        neutralVideoClip.stop()  # ensure movie has stopped at end of Routine
        # store data for trials (TrialHandler)
        trials.addData('mouse_3.x', mouse_3.x)
        trials.addData('mouse_3.y', mouse_3.y)
        trials.addData('mouse_3.leftButton', mouse_3.leftButton)
        trials.addData('mouse_3.midButton', mouse_3.midButton)
        trials.addData('mouse_3.rightButton', mouse_3.rightButton)
        trials.addData('mouse_3.time', mouse_3.time)
        # This is generated by the writeRoutineEndCode
        # the Routine "neutralVideo" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
    # completed 1.0 repeats of 'trials'
    
    # Run 'End Experiment' code from code

    core.wait(1) # Wait for EEG data to be packaged
    cortex_obj.close_session()
    # Run 'End Experiment' code from code_2
    # Code inserted in positivenegative, end experiment section
    print('Here in end experiment for attractiveness')
    
    # mark experiment as finished
    endExperiment(thisExp, win=win, inputs=inputs)


def saveData(thisExp):
    """
    Save data from this experiment
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    filename = thisExp.dataFileName
    # these shouldn't be strictly necessary (should auto-save)
    thisExp.saveAsWideText(filename + '.csv', delim='auto')
    thisExp.saveAsPickle(filename)


def endExperiment(thisExp, inputs=None, win=None):
    """
    End this experiment, performing final shut down operations.
    
    This function does NOT close the window or end the Python process - use `quit` for this.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    inputs : dict
        Dictionary of input devices by name.
    win : psychopy.visual.Window
        Window for this experiment.
    """
    if win is not None:
        # remove autodraw from all current components
        win.clearAutoDraw()
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed
        win.flip()
    # mark experiment handler as finished
    thisExp.status = FINISHED
    # shut down eyetracker, if there is one
    if inputs is not None:
        if 'eyetracker' in inputs and inputs['eyetracker'] is not None:
            inputs['eyetracker'].setConnectionState(False)
    logging.flush()


def quit(thisExp, win=None, inputs=None, thisSession=None):
    global ffmpeg_process
    """
    Fully quit, closing the window and ending the Python process.
    
    Parameters
    ==========
    win : psychopy.visual.Window
        Window to close.
    inputs : dict
        Dictionary of input devices by name.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    thisExp.abort()  # or data files will save again on exit
    # make sure everything is closed down
    if win is not None:
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed before quitting
        win.flip()
        win.close()
    if inputs is not None:
        if 'eyetracker' in inputs and inputs['eyetracker'] is not None:
            inputs['eyetracker'].setConnectionState(False)
    logging.flush()
    if ffmpeg_process.poll() is None:
        print("Terminating ffmpeg subprocess...")
        ffmpeg_process.terminate()
        print('Terminated Process')
        ffmpeg_process.wait()  # Wait for the subprocess to finish
        print('After process.wait')
    if thisSession is not None:
        thisSession.stop()
    # terminate Python process
    core.quit()


# if running this experiment as a script...
if __name__ == '__main__':
    # call all functions in order
    expInfo = showExpInfoDlg(expInfo=expInfo)
    thisExp = setupData(expInfo=expInfo)
    logFile = setupLogging(filename=thisExp.dataFileName)
    win = setupWindow(expInfo=expInfo)
    inputs = setupInputs(expInfo=expInfo, thisExp=thisExp, win=win)
    run(
        expInfo=expInfo, 
        thisExp=thisExp, 
        win=win, 
        inputs=inputs
    )
    saveData(thisExp=thisExp)
    quit(thisExp=thisExp, win=win, inputs=inputs)