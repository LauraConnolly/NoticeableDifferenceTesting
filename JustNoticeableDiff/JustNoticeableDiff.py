import logging
import os

import vtk
import qt
import slicer
from slicer.ScriptedLoadableModule import *
from slicer.util import VTKObservationMixin
import random
from functools import partial
import csv
import numpy as np

#
# JustNoticeableDiff
#

class JustNoticeableDiff(ScriptedLoadableModule):
    """Uses ScriptedLoadableModule base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = "JustNoticeableDiff"  # TODO: make this more human readable by adding spaces
        self.parent.categories = ["Examples"]  # TODO: set categories (folders where the module shows up in the module selector)
        self.parent.dependencies = []  # TODO: add here list of module names that this module requires
        self.parent.contributors = ["John Doe (AnyWare Corp.)"]  # TODO: replace with "Firstname Lastname (Organization)"
        # TODO: update with short description of the module and a link to online module documentation
        self.parent.helpText = """
This is an example of scripted loadable module bundled in an extension.
See more information in <a href="https://github.com/organization/projectname#JustNoticeableDiff">module documentation</a>.
"""
        # TODO: replace with organization, grant and thanks
        self.parent.acknowledgementText = """
This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc., Andras Lasso, PerkLab,
and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
"""

        # Additional initialization step after application startup is complete
        slicer.app.connect("startupCompleted()", registerSampleData)


#
# Register sample data sets in Sample Data module
#

def registerSampleData():
    """
    Add data sets to Sample Data module.
    """
    # It is always recommended to provide sample data for users to make it easy to try the module,
    # but if no sample data is available then this method (and associated startupCompeted signal connection) can be removed.

    import SampleData
    iconsPath = os.path.join(os.path.dirname(__file__), 'Resources/Icons')

    # To ensure that the source code repository remains small (can be downloaded and installed quickly)
    # it is recommended to store data sets that are larger than a few MB in a Github release.

    # JustNoticeableDiff1
    SampleData.SampleDataLogic.registerCustomSampleDataSource(
        # Category and sample name displayed in Sample Data module
        category='JustNoticeableDiff',
        sampleName='JustNoticeableDiff1',
        # Thumbnail should have size of approximately 260x280 pixels and stored in Resources/Icons folder.
        # It can be created by Screen Capture module, "Capture all views" option enabled, "Number of images" set to "Single".
        thumbnailFileName=os.path.join(iconsPath, 'JustNoticeableDiff1.png'),
        # Download URL and target file name
        uris="https://github.com/Slicer/SlicerTestingData/releases/download/SHA256/998cb522173839c78657f4bc0ea907cea09fd04e44601f17c82ea27927937b95",
        fileNames='JustNoticeableDiff1.nrrd',
        # Checksum to ensure file integrity. Can be computed by this command:
        #  import hashlib; print(hashlib.sha256(open(filename, "rb").read()).hexdigest())
        checksums='SHA256:998cb522173839c78657f4bc0ea907cea09fd04e44601f17c82ea27927937b95',
        # This node name will be used when the data set is loaded
        nodeNames='JustNoticeableDiff1'
    )

    # JustNoticeableDiff2
    SampleData.SampleDataLogic.registerCustomSampleDataSource(
        # Category and sample name displayed in Sample Data module
        category='JustNoticeableDiff',
        sampleName='JustNoticeableDiff2',
        thumbnailFileName=os.path.join(iconsPath, 'JustNoticeableDiff2.png'),
        # Download URL and target file name
        uris="https://github.com/Slicer/SlicerTestingData/releases/download/SHA256/1a64f3f422eb3d1c9b093d1a18da354b13bcf307907c66317e2463ee530b7a97",
        fileNames='JustNoticeableDiff2.nrrd',
        checksums='SHA256:1a64f3f422eb3d1c9b093d1a18da354b13bcf307907c66317e2463ee530b7a97',
        # This node name will be used when the data set is loaded
        nodeNames='JustNoticeableDiff2'
    )


#
# JustNoticeableDiffWidget
#

class JustNoticeableDiffWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):
    """Uses ScriptedLoadableModuleWidget base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent=None):
        """
        Called when the user opens the module the first time and the widget is initialized.
        """
        ScriptedLoadableModuleWidget.__init__(self, parent)
        VTKObservationMixin.__init__(self)  # needed for parameter node observation
        self.logic = None
        self._parameterNode = None
        self._updatingGUIFromParameterNode = False

    def setup(self):
        """
        Called when the user opens the module the first time and the widget is initialized.
        """
        ScriptedLoadableModuleWidget.setup(self)

        # Load widget from .ui file (created by Qt Designer).
        # Additional widgets can be instantiated manually and added to self.layout.
        uiWidget = slicer.util.loadUI(self.resourcePath('UI/JustNoticeableDiff.ui'))
        self.layout.addWidget(uiWidget)
        self.ui = slicer.util.childWidgetVariables(uiWidget)

        # Set scene in MRML widgets. Make sure that in Qt designer the top-level qMRMLWidget's
        # "mrmlSceneChanged(vtkMRMLScene*)" signal in is connected to each MRML widget's.
        # "setMRMLScene(vtkMRMLScene*)" slot.
        uiWidget.setMRMLScene(slicer.mrmlScene)

        # Create logic class. Logic implements all computations that should be possible to run
        # in batch mode, without a graphical user interface.
        self.logic = JustNoticeableDiffLogic()

        self.ui.initializePublisherButton.connect('clicked(bool)', self.onInitializePublisherButtonClicked)
        self.ui.publishForceButton.connect('clicked(bool)', self.onPublishForceButtonClicked)

        self.ui.startFMinTestButton.connect('clicked(bool)', self.onStartFMinTestButton)
        self.ui.forceDetectedButton.connect('clicked(bool)', self.onForceDetectedButton)
        self.ui.restartMinimumForceTestingButton.connect('clicked(bool)', self.onRestartForceMinimumButton)

        self.ui.startDeltaFTestButton.connect('clicked(bool)', self.onStartDeltaFTestButton)

        self.ui.higherButton.connect('clicked(bool)', self.onHigherButton)
        self.ui.sameButton.connect('clicked(bool)', self.onSameButton)
        self.ui.lowerButton.connect('clicked(bool)', self.onLowerButton)

        self.ui.compileResultsButton.connect('clicked(bool)', self.onCompileResultsButton)

        self.ui.resetForceIncrementButton.connect('clicked(bool)', self.onResetForceIncrementsButton)

        # These connections ensure that we update parameter node when scene is closed
        self.addObserver(slicer.mrmlScene, slicer.mrmlScene.StartCloseEvent, self.onSceneStartClose)
        self.addObserver(slicer.mrmlScene, slicer.mrmlScene.EndCloseEvent, self.onSceneEndClose)

        # Incremental test buttons
        self.ui.initializeForceTestingButton.connect('clicked(bool)', self.inializeForce) # IN THE MIDDLE!
        self.ui.startIncreaseForceButton.connect('clicked(bool)', self.onStartIncreaseForceButton)
        self.ui.increasedChangeDetected.connect('clicked(bool)', self.onIncreasedChangeDetection)

        self.ui.startDecreaseForceTesting.connect('clicked(bool)', self.onStartDecreaseForceButton)
        self.ui.decreaseChangeDetected.connect('clicked(bool)', self.onDecreaseChangeDetection)

        self.ui.nextReferenceForceButton.connect('clicked(bool)', self.onNextReferenceForceButton)

        self.ui.redoLastTestButton.connect('clicked(bool)', self.onRedoLastTestButton)

        self.ui.fixButtonsButton.connect('clicked(bool)', self.onFixButtons)

        # Make sure parameter node is initialized (needed for module reload)
        self.initializeParameterNode()

    def cleanup(self):
        """
        Called when the application closes and the module widget is destroyed.
        """
        self.removeObservers()

    def enter(self):
        """
        Called each time the user opens this module.
        """
        # Make sure parameter node exists and observed
        self.initializeParameterNode()

    def exit(self):
        """
        Called each time the user opens a different module.
        """
        # Do not react to parameter node changes (GUI wlil be updated when the user enters into the module)
        self.removeObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self.updateGUIFromParameterNode)

    def onSceneStartClose(self, caller, event):
        """
        Called just before the scene is closed.
        """
        # Parameter node will be reset, do not use it anymore
        self.setParameterNode(None)

    def onSceneEndClose(self, caller, event):
        """
        Called just after the scene is closed.
        """
        # If this module is shown while the scene is closed then recreate a new parameter node immediately
        if self.parent.isEntered:
            self.initializeParameterNode()

    def initializeParameterNode(self):
        """
        Ensure parameter node exists and observed.
        """
        # Parameter node stores all user choices in parameter values, node selections, etc.
        # so that when the scene is saved and reloaded, these settings are restored.

        self.setParameterNode(self.logic.getParameterNode())

        # Select default input nodes if nothing is selected yet to save a few clicks for the user
        if not self._parameterNode.GetNodeReference("InputVolume"):
            firstVolumeNode = slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLScalarVolumeNode")
            if firstVolumeNode:
                self._parameterNode.SetNodeReferenceID("InputVolume", firstVolumeNode.GetID())

    def setParameterNode(self, inputParameterNode):
        """
        Set and observe parameter node.
        Observation is needed because when the parameter node is changed then the GUI must be updated immediately.
        """

        if inputParameterNode:
            self.logic.setDefaultParameters(inputParameterNode)

        # Unobserve previously selected parameter node and add an observer to the newly selected.
        # Changes of parameter node are observed so that whenever parameters are changed by a script or any other module
        # those are reflected immediately in the GUI.
        if self._parameterNode is not None:
            self.removeObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self.updateGUIFromParameterNode)
        self._parameterNode = inputParameterNode
        if self._parameterNode is not None:
            self.addObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self.updateGUIFromParameterNode)

        # Initial GUI update
        self.updateGUIFromParameterNode()

    def updateGUIFromParameterNode(self, caller=None, event=None):
        """
        This method is called whenever parameter node is changed.
        The module GUI is updated to show the current state of the parameter node.
        """

        if self._parameterNode is None or self._updatingGUIFromParameterNode:
            return

        # Make sure GUI changes do not call updateParameterNodeFromGUI (it could cause infinite loop)
        self._updatingGUIFromParameterNode = True


        # All the GUI updates are done
        self._updatingGUIFromParameterNode = False

        if self.logic.referenceForce <= 0.3:
            self.ui.startDecreaseForceTesting.setEnabled(False)
            self.ui.decreaseChangeDetected.setEnabled(False)
        elif self.logic.referenceForce > 0.3:
            self.ui.startDecreaseForceTesting.setEnabled(True)
            self.ui.decreaseChangeDetected.setEnabled(True)

        if self.logic.referenceForce >= 3.0:
            self.ui.startIncreaseForceButton.setEnabled(False)
            self.ui.increasedChangeDetected.setEnabled(False)
        elif self.logic.referenceForce < 3.0:
            self.ui.startIncreaseForceButton.setEnabled(True)
            self.ui.increasedChangeDetected.setEnabled(True)


    def onFixButtons(self):

        self.ui.startIncreaseForceButton.setEnabled(True)
        self.ui.increasedChangeDetected.setEnabled(True)
        self.ui.startDecreaseForceTesting.setEnabled(True)
        self.ui.decreaseChangeDetected.setEnabled(True)

    def updateParameterNodeFromGUI(self, caller=None, event=None):
        """
        This method is called when the user makes any change in the GUI.
        The changes are saved into the parameter node (so that they are restored when the scene is saved and loaded).
        """

        if self._parameterNode is None or self._updatingGUIFromParameterNode:
            return

        wasModified = self._parameterNode.StartModify()  # Modify all properties in a single batch

        self._parameterNode.EndModify(wasModified)

    def onInitializePublisherButtonClicked(self):

        self.logic.initializePublisher()

    def onPublishForceButtonClicked(self):

        self.logic.publishForce(self.ui.forceInputSpinBox.value)

    def onStartFMinTestButton(self):

        self.logic.startForceMinimumTesting()

    def onForceDetectedButton(self):

        self.logic.forceDetected()

    def onStartDeltaFTestButton(self):

        self.logic.startDeltaFTest()

    def onHigherButton(self):

        self.logic.higherButtonClicked()

    def onSameButton(self):

        self.logic.sameButtonClicked()

    def onLowerButton(self):

        self.logic.lowerButtonClicked()

    def onCompileResultsButton(self):

        # self.logic.compileResultsButtonClicked()
        # self.logic.saveResults(self.ui.saveResultLineEdit.text, self.ui.trialNumberSpinBox.value)
        self.logic.compileGradualResultsButtonClicked()
        self.logic.saveGradualForceResults(self.ui.saveResultLineEdit.text, self.ui.trialNumberSpinBox.value)

    def onResetForceIncrementsButton(self):

        self.logic.resetForceIncrements()

    def onStartIncreaseForceButton(self):

        self.logic.startGradualForceTest()

    def onIncreasedChangeDetection(self):

        self.logic.increasedChangeDetected()

    def inializeForce(self):

        self.logic.initializeGradualForceTest()

    def onStartDecreaseForceButton(self):

        self.logic.startGradualForceTestDecrease()

    def onDecreaseChangeDetection(self):

        self.logic.decreasedChangeDetected()

    def onNextReferenceForceButton(self):

        self.logic.nextReferenceForceButton()

    def onRestartForceMinimumButton(self):

        self.logic.minimumForce = 0.0
        self.logic.index = 0
        self.logic.force = self.logic.forces[self.logic.index]
        self.logic.startForceMinimumTesting()

    def onRedoLastTestButton(self):

        self.logic.redoLastTest()




#
# JustNoticeableDiffLogic
#

class JustNoticeableDiffLogic(ScriptedLoadableModuleLogic):
    """This class should implement all the actual
    computation done by your module.  The interface
    should be such that other python code can import
    this class and make use of the functionality without
    requiring an instance of the Widget.
    Uses ScriptedLoadableModuleLogic base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self):
        """
        Called when the logic class is instantiated. Can be used for initializing member variables.
        """
        ScriptedLoadableModuleLogic.__init__(self)
        self.forcePublisher = None
        self.timer = None
        self.forces = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2, 3.3]
        self.forceIncrements = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, -0.1, -0.2, -0.3, -0.4, -0.5, -0.6, -0.7, -0.8, -0.9, -1.0]
        self.index = 0
        self.minimumForce = 0
        self.maximumForce = 3.3
        self.startingForce = 0
        self.updatedForce = 0
        self.feedback_received = None

        self.deltaFTimer = qt.QTimer()

        self.results = []

        # gradual force increase test
        self.forceRange = []
        self.gradualindex = 0
        self.forceIncrementCounter = 0
        self.gradualForceTestIndexCounter = 0

        self.gradualIncreaseTimer = qt.QTimer()
        self.gradualDecreaseTimer = qt.QTimer()
        self.referenceForce = 0


    def resetForceIncrements(self):

        self.forceIncrements = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, -0.1, -0.2, -0.3, -0.4, -0.5, -0.6, -0.7, -0.8, -0.9, -1.0]

    def setDefaultParameters(self, parameterNode):
        """
        Initialize parameter node with default settings.
        """
        if not parameterNode.GetParameter("Threshold"):
            parameterNode.SetParameter("Threshold", "100.0")
        if not parameterNode.GetParameter("Invert"):
            parameterNode.SetParameter("Invert", "false")
        self.parameterNode = parameterNode

    def initializePublisher(self):

        ros = slicer.util.getModuleLogic('ROS2')
        node = ros.GetDefaultROS2Node()
        self.forcePublisher = node.CreateAndAddPublisherNode('vtkMRMLROS2PublisherWrenchStampedNode', '/arm/servo_cf')
        self.force = 0

    def publishForce(self, forceValue):

        double_array = vtk.vtkDoubleArray()
        double_array.SetNumberOfValues(6)
        forceComponent = forceValue / np.sqrt(3)
        double_array.SetValue(0, forceComponent)
        double_array.SetValue(1, forceComponent)
        double_array.SetValue(2, forceComponent)
        double_array.SetValue(3, 0)
        double_array.SetValue(4, 0)
        double_array.SetValue(5, 0)

        print("Published force: {}".format(forceValue))

        pub = slicer.mrmlScene.GetFirstNodeByName('ros2:pub:/arm/servo_cf')
        pub.Publish(double_array)

        parameterNode = self.getParameterNode()
        parameterNode.Modified()


    def startForceMinimumTesting(self):

        self.timer = qt.QTimer()
        self.timer.setInterval(3000)
        self.timer.timeout.connect(self.sendForce)
        self.timer.start()

    def sendForce(self):

        if self.force == 3.3:
            self.timer.stop()
            self.force = 0

        self.publishForce(self.force)
        self.force = self.forces[self.index]
        self.index = self.index + 1

    def forceDetected(self):

        self.timer.stop()
        print("Minimum force detected: {}".format(self.force - 0.1))
        self.minimumForce = self.force - 0.1

        result = {
            "Minimum Force Detect": self.minimumForce,
        }
        self.results.append(result)
        parameterNode = self.getParameterNode()
        parameterNode.Modified()

    def startDeltaFTest(self):

        delay_ms = 2000  # 3 seconds
        self.startingForce = round(random.uniform(self.minimumForce, self.maximumForce) * 10) / 10

        print(len(self.forceIncrements))

        forceIncrement = random.choice(self.forceIncrements)
        self.forceIncrements.remove(forceIncrement)
        self.updatedForce = self.startingForce + forceIncrement
        # print("Starting force: {}".format(self.startingForce))
        # print("Updated force: {}".format(self.updatedForce))
        forces = [self.startingForce, self.updatedForce]
        self.publishForce(0)
        # Create timers in a loop
        for i, force in enumerate(forces):
            self.deltaFTimer.singleShot((len(forces) + i) * delay_ms, partial(self.deltaF_test, force=force, index=i))

    def deltaF_test(self, force, index):
        if force > 3.3:
            force = 3.3
        if force < self.minimumForce:
            force = self.minimumForce
        # print("Delta f test happening, applied force :{}".format(force))
        print("Delta f test happening, applied force")
        self.publishForce(force)


    def receive_feedback(self, feedback):
        """
        Called when the user provides feedback via the GUI.
        """
        if self.startingForce is not None:
            result = {
                "Starting Force": self.startingForce,
                "Updated Force": self.updatedForce,
                "Feedback": feedback,  # Feedback should be "higher", "same", or "lower"
            }
            self.results.append(result)
            self.feedback_received = True
            print(f"Feedback received: {feedback}")
            # print(len(self.results))

    def recieve_gradual_feedback(self, increase, decrease):

        # Note the - 1 is because the function automatically iterates the counter
        combinedForce = 0
        delta = 0
        if increase == True:
            combinedForce = self.forceRange[self.forceIncrementCounter] + self.gradualForceIncrements[self.gradualForceTestIndexCounter - 1]
            delta = self.gradualForceIncrements[self.gradualForceTestIndexCounter - 1]
        elif increase == False:
            combinedForce = self.forceRange[self.forceIncrementCounter] - self.gradualForceIncrements[self.gradualForceTestIndexCounter - 1]
            delta = -self.gradualForceIncrements[self.gradualForceTestIndexCounter - 1]
        result = {
            "Reference force": self.forceRange[self.forceIncrementCounter],
            "Detected delta": delta,
            "Combined force": combinedForce,  # Feedback should be "higher", "same", or "lower"
        }
        self.results.append(result)
        self.feedback_received = True
        print(f"Feedback received.")


    def higherButtonClicked(self):

        self.feedback_received = "Higher"
        self.receive_feedback("Higher")

    def lowerButtonClicked(self):

        self.feedback_received = "Lower"
        self.receive_feedback("Lower")

    def sameButtonClicked(self):

        self.feedback_received = "Same"
        self.receive_feedback("Same")

    def frange(self, start, stop, step):
        """Generate values in a floating-point range with a given step size."""
        while start <= stop:
            yield start
            start += step

    def initializeGradualForceTest(self):

        self.forceRange = [round(f, 1) for f in np.linspace(self.minimumForce, self.maximumForce, 5)]
        self.forceIncrementCounter = 0
        self.gradualForceTestIndexCounter = 0
        self.gradualForceIncrements = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0]
        print("Force range: {}".format(self.forceRange))

    def startGradualForceTest(self):

        # here set force ref and then start the timer to gradually add 0.2 N in the positive direction
        self.gradualIncreaseTimer = qt.QTimer()
        self.gradualIncreaseTimer.setInterval(3000)
        self.gradualIncreaseTimer.timeout.connect(self.sendGradual)
        self.gradualIncreaseTimer.start()

    def startGradualForceTestDecrease(self):

        self.gradualIncreaseTimer = qt.QTimer()
        self.gradualIncreaseTimer.setInterval(3000)
        self.gradualIncreaseTimer.timeout.connect(self.sendGradualDecrease)
        self.gradualIncreaseTimer.start()

    def sendGradual(self):

        # Loop through the gradual force increments on the reference force
        self.referenceForce = self.forceRange[self.forceIncrementCounter]
        new_force = self.referenceForce + self.gradualForceIncrements[self.gradualForceTestIndexCounter]
        if new_force > 3.3:
            print("Force limit reached")
            self.increasedChangeDetected()
            return
        self.publishForce(self.referenceForce + self.gradualForceIncrements[self.gradualForceTestIndexCounter])
        print("Gradual force test increment: {}".format(self.gradualForceIncrements[self.gradualForceTestIndexCounter]))
        self.gradualForceTestIndexCounter = self.gradualForceTestIndexCounter + 1

    def sendGradualDecrease(self):

        # Loop through the gradual force increments on the reference force
        self.referenceForce = self.forceRange[self.forceIncrementCounter]
        new_force = self.referenceForce - self.gradualForceIncrements[self.gradualForceTestIndexCounter]
        if new_force < 0.1:
            print("Force minimum reached")
            self.decreasedChangeDetected()
            return
        self.publishForce(self.referenceForce - self.gradualForceIncrements[self.gradualForceTestIndexCounter])
        print("Gradual force test increment: {}".format(self.gradualForceIncrements[self.gradualForceTestIndexCounter]))
        self.gradualForceTestIndexCounter = self.gradualForceTestIndexCounter + 1


    def increasedChangeDetected(self):

        # Stop the timer and save the delta and the reference force
        print("increased change detected")
        self.gradualIncreaseTimer.stop()

        self.recieve_gradual_feedback(True, False)

        self.gradualForceTestIndexCounter = 0


    def decreasedChangeDetected(self):

        print("decreased change detected")
        self.gradualIncreaseTimer.stop()

        self.recieve_gradual_feedback(False, True)

        self.gradualForceTestIndexCounter = 0



    def nextReferenceForceButton(self):

        self.forceIncrementCounter = self.forceIncrementCounter + 1
        parameterNode = self.getParameterNode()
        parameterNode.Modified()

    def compileResultsButtonClicked(self):

        print("Compiled results: {}".format(self.results))

    def saveResults(self, user, trial_number):

        if user == "":
            number = random.randrange(1,100)
            user = "User" + str(number)
        csv_file_name = "/home/lauraconnolly/Documents/VirtualFixture/VF_testing/Results/User_" + user + "_trial" + str(trial_number) + "_minimumForce" + str(self.minimumForce) + "_results.csv"
        fieldnames = ["Minimum Force Detect", "Starting Force", "Updated Force", "Feedback"]
        # Write the list of dictionaries to a CSV file
        with open(csv_file_name, mode="w", newline="") as csv_file:
            # Create a CSV writer object
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            # Write the header row
            writer.writeheader()

            # Write the data rows
            writer.writerows(self.results)

        print(f"Data saved to {csv_file_name}")

    def compileGradualResultsButtonClicked(self):

        print("Compiled results: {}".format(self.results))

    def saveGradualForceResults(self, user, trial_number):

        if user == "":
            number = random.randrange(1,100)
            user = "User" + str(number)
        csv_file_name = "/home/lauraconnolly/Documents/VirtualFixture/VF_testing/Results/Gradual_User_" + user + "_trial" + str(trial_number) + "_minimumForce" + str(self.minimumForce) + "_results.csv"
        fieldnames = ["Minimum Force Detect", "Reference force", "Detected delta", "Combined force"]
        # Write the list of dictionaries to a CSV file
        with open(csv_file_name, mode="w", newline="") as csv_file:
            # Create a CSV writer object
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            # Write the header row
            writer.writeheader()

            # Write the data rows
            writer.writerows(self.results)

        print(f"Data saved to {csv_file_name}")


    def redoLastTest(self):

        self.gradualIncreaseTimer.stop()
        self.gradualForceTestIndexCounter = 0




        #
# JustNoticeableDiffTest
#

class JustNoticeableDiffTest(ScriptedLoadableModuleTest):
    """
    This is the test case for your scripted module.
    Uses ScriptedLoadableModuleTest base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def setUp(self):
        """ Do whatever is needed to reset the state - typically a scene clear will be enough.
        """
        slicer.mrmlScene.Clear()

    def runTest(self):
        """Run as few or as many tests as needed here.
        """
        self.setUp()
        self.test_JustNoticeableDiff1()

    def test_JustNoticeableDiff1(self):
        """ Ideally you should have several levels of tests.  At the lowest level
        tests should exercise the functionality of the logic with different inputs
        (both valid and invalid).  At higher levels your tests should emulate the
        way the user would interact with your code and confirm that it still works
        the way you intended.
        One of the most important features of the tests is that it should alert other
        developers when their changes will have an impact on the behavior of your
        module.  For example, if a developer removes a feature that you depend on,
        your test should break so they know that the feature is needed.
        """

        self.delayDisplay("Starting the test")

        # Get/create input data

        import SampleData
        registerSampleData()
        inputVolume = SampleData.downloadSample('JustNoticeableDiff1')
        self.delayDisplay('Loaded test data set')

        inputScalarRange = inputVolume.GetImageData().GetScalarRange()
        self.assertEqual(inputScalarRange[0], 0)
        self.assertEqual(inputScalarRange[1], 695)

        outputVolume = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLScalarVolumeNode")
        threshold = 100

        # Test the module logic

        logic = JustNoticeableDiffLogic()

        # Test algorithm with non-inverted threshold
        logic.process(inputVolume, outputVolume, threshold, True)
        outputScalarRange = outputVolume.GetImageData().GetScalarRange()
        self.assertEqual(outputScalarRange[0], inputScalarRange[0])
        self.assertEqual(outputScalarRange[1], threshold)

        # Test algorithm with inverted threshold
        logic.process(inputVolume, outputVolume, threshold, False)
        outputScalarRange = outputVolume.GetImageData().GetScalarRange()
        self.assertEqual(outputScalarRange[0], inputScalarRange[0])
        self.assertEqual(outputScalarRange[1], inputScalarRange[1])

        self.delayDisplay('Test passed')
