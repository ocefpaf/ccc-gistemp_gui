#!/usr/bin/env python
# $URL$
# $Rev$
#
# run_gui.py
#
# Filipe Fernandes, 2011-06-20

""" Graphical user interface to run ccc-gistemp and visualize its outputs."""

# http://docs.python.org/release/2.4.4/lib/module-os.path.html
import os
# http://www.python.org/doc/2.4.4/lib/module-sys.html
import sys
# http://docs.python.org/release/2.4.4/lib/module-glob.html
import glob
# http://docs.python.org/release/2.4.4/lib/module-urllib.html
import urllib
# http://docs.python.org/release/2.4.4/lib/module-webbrowser.html
import webbrowser

# http://www.wxpython.org/onlinedocs.php
import wx
from wxPython.lib.dialogs import wxScrolledMessageDialog

# Clear Climate Code
from CCCgistemp.tool import run
from CCCgistemp.tool.vischeck import anom, annual_anomalies, asgooglechartURL
from CCCgistemp.code.read_config import generate_defaults
import gui.lib.packaging as pkg
from gui.lib.gistemp2csv import gistemp2csv

# http://bazaar.launchpad.net/~stani/phatch/trunk/view/head:/phatch/lib/notify
from gui.lib import notify

__docformat__ = "restructuredtext"

# -----------------------------------------------------------------------------
# Constants
WIDTH, HEIGHT = 920, 600
HEADER_W, HEADER_H = 900, 150

# Get approot directory.
SETUP = pkg.get_setup()
if SETUP == 'source':  # not frozen
    APPROOT = os.path.join(os.getcwd(), os.path.dirname(__file__))
elif SETUP == 'py2exe':
    APPROOT = os.path.dirname(sys.executable)
elif SETUP == 'py2app':
    APPROOT = os.environ['RESOURCEPATH']
elif SETUP == 'packaged':
    APPROOT = "/usr/share"  # Linux
else:
    print("Failed to get APPROOT.")


# Resources (icons and figures.)
def app_root_path(filename):
    """Join App root path with the file name."""
    return os.path.join(APPROOT, filename)

if SETUP == 'source':
    APPROOT = app_root_path('resources')

HEADER_FILE = app_root_path('ccf-header.png')
ICO = app_root_path('ccf.ico')
SPLASH = app_root_path('splash.png')


# -----------------------------------------------------------------------------
class RedirectText(object):
    """Redirect text to a wxTextCtrl frame."""

    def __init__(self, aWxTextCtrl):
        self.out = aWxTextCtrl

    def write(self, string):
        wx.CallAfter(self.out.WriteText, string)
        wx.Yield()

    def flush(self):
        """Sometimes stdout is called with the flush() method."""
        wx.Yield()
        pass


class MySplashScreen(wx.SplashScreen):
    """Create a splash screen widget."""
    def __init__(self, parent=None):
        self.bitmap = wx.Bitmap(SPLASH, wx.BITMAP_TYPE_PNG)
        shadow = wx.WHITE
        splashStyle = wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT
        splashDuration = 1000  # milliseconds
        wx.SplashScreen.__init__(self, self.bitmap, splashStyle,
                                 splashDuration, parent)
        self.Bind(wx.EVT_CLOSE, self.OnExit)
        wx.Yield()

    def OnExit(self, event):
        self.Hide()
        MyFrame = Frame()
        app.SetTopWindow(MyFrame)
        MyFrame.Show(True)
        # The program will freeze without this line.
        event.Skip()


class App(wx.App):
    """Create the application class with a splash screen at initialization."""
    def OnInit(self):
        MySplash = MySplashScreen()
        MySplash.Show()
        return True


# Frame class
class Frame(wx.Frame):
    """Main GUI window."""
    def __init__(self, parent=None, id=-1):
        wx.Frame.__init__(self, parent, id=-1, title='ccc-gistemp',
                          size=(WIDTH, HEIGHT), pos=wx.DefaultPosition)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        # ---------------------------------------------------------------------
        # Top left icon.
        icon = wx.Icon(name=ICO, type=wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        # ---------------------------------------------------------------------
        # Main panel.
        self.panel = wx.Panel(self, size=(WIDTH, HEIGHT))
        self.panel.SetBackgroundColour(wx.WHITE)

        # ---------------------------------------------------------------------
        # Menu bar.
        menubar = wx.MenuBar()

        filemenu = wx.Menu()
        helpmenu = wx.Menu()

        open_proj = filemenu.Append(wx.NewId(), '&Open Project directory...')
        crea_proj = filemenu.Append(wx.NewId(), '&Create Project directory...')
        open_csv = filemenu.Append(wx.NewId(), '&Open spreadsheet results...')

        filemenu.AppendSeparator()
        filemenu.Append(wx.ID_EXIT, "E&xit", "Terminate the program")

        help_proj = helpmenu.Append(wx.NewId(), 'Help')
        dwl_info = helpmenu.Append(wx.NewId(), '&Download info')
        about = helpmenu.Append(wx.ID_ABOUT,
                              "&About",
                              "More information about this program")

        menubar.Append(filemenu, '&File')
        menubar.Append(helpmenu, '&Help')

        self.SetMenuBar(menubar)

        wx.EVT_MENU(self, wx.ID_EXIT,  self.OnClose)
        wx.EVT_MENU(self, wx.ID_ABOUT,  self.OnAbout)
        wx.EVT_MENU(self, open_proj.GetId(),  self.OnDir)
        wx.EVT_MENU(self, open_csv.GetId(),  self.OnCSV)
        wx.EVT_MENU(self, dwl_info.GetId(),  self.OnDownloadInfo)
        # TODO: For now it is the same as open_proj, since a new
        # project is just a new directory with the config directory. However,
        # if we ever create a more sophisticated project management scheme this
        # must be improved. Also, a validated_open_prj() should be created
        # to check the results of a previous run.
        wx.EVT_MENU(self, crea_proj.GetId(),  self.OnDir)
        # NOTE (m): overwrite a previous run without warning.

        # ---------------------------------------------------------------------
        # Header (also a button to the source code.)
        pic = wx.Image(name=HEADER_FILE, type=wx.BITMAP_TYPE_PNG)
        pic = pic.ConvertToBitmap()
        btn_source = wx.StaticBitmap(parent=self.panel, id=-1,
                                          bitmap=pic,
                                          pos=(0, 0),
                                          style=wx.NO_BORDER)
        btn_source.Bind(wx.EVT_LEFT_DOWN, self.webSource)

        # ---------------------------------------------------------------------
        # Text box.
        # NOTE (m): Get rid of these weird hard-coded offset numbers.
        log = wx.TextCtrl(self.panel, wx.ID_ANY,
                          size=(WIDTH - 2 * 90, HEIGHT - HEADER_H - 55),
                          pos=(90, HEADER_H + 10),
                          style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)

        # Redirect text here.
        sys.stderr = RedirectText(log)
        sys.stdout = RedirectText(log)

        # ---------------------------------------------------------------------
        # Buttons.
        offset = 30
        run_button = wx.Button(self.panel, label='Run',
                               pos=(0, HEADER_H + offset))
        stp0_button = wx.Button(self.panel, id=0, label="Step 0",
                                pos=(0, HEADER_H + 3 * offset))
        stp1_button = wx.Button(self.panel, id=1, label="Step 1",
                                pos=(0, HEADER_H + 4 * offset))
        stp2_button = wx.Button(self.panel, id=2, label="Step 2",
                                pos=(0, HEADER_H + 5 * offset))
        stp3_button = wx.Button(self.panel, id=3, label="Step 3",
                                pos=(0, HEADER_H + 6 * offset))
        stp4_button = wx.Button(self.panel, id=4, label="Step 4",
                                pos=(0, HEADER_H + 7 * offset))
        stp5_button = wx.Button(self.panel, id=5, label="Step 5",
                                pos=(0, HEADER_H + 8 * offset))
        stp6_button = wx.Button(self.panel, id=6, label="Show result",
                                pos=(0, HEADER_H + 9 * offset))
        close_button = wx.Button(self.panel, wx.ID_CLOSE, label="Exit",
                                 pos=(0, HEADER_H + 11 * offset))

        # Button action.
        run_button.Bind(wx.EVT_BUTTON, self.RunCCCgistemp)
        stp0_button.Bind(wx.EVT_BUTTON, self.RunCCCgistemp_steps)
        stp1_button.Bind(wx.EVT_BUTTON, self.RunCCCgistemp_steps)
        stp2_button.Bind(wx.EVT_BUTTON, self.RunCCCgistemp_steps)
        stp3_button.Bind(wx.EVT_BUTTON, self.RunCCCgistemp_steps)
        stp4_button.Bind(wx.EVT_BUTTON, self.RunCCCgistemp_steps)
        stp5_button.Bind(wx.EVT_BUTTON, self.RunCCCgistemp_steps)
        stp6_button.Bind(wx.EVT_BUTTON, self.OnShow)
        close_button.Bind(wx.EVT_BUTTON, self.OnClose)

        self.panel.Layout()

        self.WORK_DIR = False  # Constant to check for working directory.

    # -------------------------------------------------------------------------
    # GUI events:
    def webSource(self, event):
        """Open link for the source code."""
        url = 'http://code.google.com/p/ccc-gistemp/'
        webbrowser.open(url)

    def OnClose(self, event):
        """Close confirmation."""
        dialog = wx.MessageDialog(self,
                               "Do you want to close the application?",
                               "Confirm Exit",
                               wx.OK | wx.CANCEL | wx.ICON_QUESTION)
        result = dialog.ShowModal()
        dialog.Destroy()
        if result == wx.ID_OK:
            wx.CallAfter(self.Destroy())

    def RunCCCgistemp(self, event):
        """Full ccc-gistemp run."""
        if self.check_dir():
            notify.send(title='ccc-gistemp',
                        message='running ccc-gistemp',
                        icon=ICO)
            run.main(['dummy', '-s', '0-5'])
            notify.send(title='ccc-gistemp',
                        message='Finished ccc-gistemp run',
                        icon=ICO)
        else:
            print("Canceled by the user.")

    def RunCCCgistemp_steps(self, event):
        """Run steps."""
        step = str(event.GetId())  # NOTE (m): Dangerous use of id.

        self.onStepInfo(step)

        if self.check_dir():
            notify.send(title='ccc-gistemp',
                        message=('running ccc-gistemp step %s' % step),
                        icon=ICO)
            run.main(argv=['dummy', '-s', step])
            notify.send(title='ccc-gistemp',
                        message=('Finished ccc-gistemp step %s' % step),
                        icon=ICO)
        else:
            print("Canceled by the user.")

    def OnDir(self, event):
        """Button to change/create project directory."""
        self.WORK_DIR = self.proj_dir()
        return self.WORK_DIR

    # NOTE (c): we need an alternative way to display graphs.
    def OnShow(self, event):
        """"Show google chart url."""
        if self.check_dir():
            res_list,  res_files = self.get_result_files()
            box = wx.SingleChoiceDialog(parent=None,
                                        message="List of result",
                                        caption="Choose a result file",
                                        choices=res_list)
            if box.ShowModal() == wx.ID_OK:
                answer = box.GetStringSelection()
                idx = res_list.index(answer)
                answer = res_files[idx]
                box.Destroy()
            try:
                with open(answer) as f:
                    url = asgooglechartURL([annual_anomalies(f)])
                    webbrowser.open(url.strip())
            except IOError:
                print("Could not open result/google-chart.url")
        else:
            print("Canceled by the user.")

    def OnCSV(self, event):
        """"Show csv files with default spreadsheet program."""
        if self.check_dir():
            res_list,  res_files = self.get_result_files()
            box = wx.SingleChoiceDialog(parent=None,
                                        message="List of result",
                                        caption="Choose a result file",
                                        choices=res_list)
            if box.ShowModal() == wx.ID_OK:
                answer = box.GetStringSelection()
                idx = res_list.index(answer)
                answer = res_files[idx]
                box.Destroy()
            try:
                csv = gistemp2csv(answer)
                pkg.default_prog(csv)
            except IOError:
                print("Could not open %s" % csv)
        else:
            print("Canceled by the user.")

    def OnDownloadInfo(self, event):
        """Show information regarding the downloaded files."""
        message = open(app_root_path('GUI-help-input-files.txt'))
        self.showMessageDlg(message.read(), "Download information",
                                                wx.OK | wx.ICON_INFORMATION)
        message.close()

    def OnAbout(self, event):
        """Show about text."""
        message = open(app_root_path('GUI-about.txt'))
        self.showMessageDlg(message.read(), "About",
                            wx.OK | wx.ICON_INFORMATION)
        message.close()

    # -------------------------------------------------------------------------
    # Methods.
    def showMessageDlg(self, message, title, style):
        """Wrapper for dialog messages."""
        dialog = wxScrolledMessageDialog(parent=None, msg=message,
                                caption=title, style=style)
        answer = dialog.ShowModal()
        dialog.Destroy()
        return answer

    def onStepInfo(self, step):
        """Show information regarding the step process."""
        text = 'GUI-step' + step + '.txt'
        with open(app_root_path(text)) as msg:
            self.showMessageDlg(msg.read(), "Step information.",
                                wx.OK | wx.ICON_INFORMATION)

    def check_dir(self):
        """ Check if inside a working directory.
        If not create one and change to it.
        """
        if not self.WORK_DIR:
            self.showMessageDlg("Choose or create a project directory",
                                "Information", wx.OK | wx.ICON_INFORMATION)
            self.WORK_DIR = self.proj_dir()
            return self.WORK_DIR
        else:
            return self.WORK_DIR

    def get_result_files(self):
        """Return a list and the paths of the result text files."""
        res_files = glob.glob(os.path.join(self.CURR_DIR, 'result', '*.txt'))
        res_list = [os.path.basename(l) for l in res_files]
        return res_list, res_files

    def deploy_config(self):
        """Add config directory if it does not exists.
        NOTE (c): Open a text editor so the user can modify these files.
        """
        if self.WORK_DIR:
            config_hk = generate_defaults()
            if config_hk['directory']:
                print("\nCreated config directory.")
            if config_hk['step1_adjust']:
                print("\nCreated step1_adjust config file.")
            if config_hk['Ts.strange.RSU.list.IN']:
                print("\nCreated Ts.strange.RSU.list.IN config file.")

    def proj_dir(self):
        """Create a project directory and change to it."""
        dialog = wx.DirDialog(self,
                           message="Choose/Create project a directory:",
                           style=wx.DD_NEW_DIR_BUTTON | wx.DD_CHANGE_DIR)

        if dialog.ShowModal() == wx.ID_OK:
            self.CURR_DIR = dialog.GetPath()
            print("Created project directory at:\n\t%s" % self.CURR_DIR)
            self.WORK_DIR = True
            self.deploy_config()
        else:
            self.WORK_DIR = False

        dialog.Destroy()
        return self.WORK_DIR


# NOTE: I do not know why the splash screen does not work when using main()
app = App(redirect=False)
app.MainLoop()

if 0:
    def main():
        app = App(redirect=False)
        app.MainLoop()

    if __name__ == '__main__':
        main()
