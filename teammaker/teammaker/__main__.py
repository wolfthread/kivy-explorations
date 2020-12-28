"""
Principal module of teammaker package. Executed at the start of the program.
"""

import teammakergui

if __name__ == '__main__':
    """
        Entry point. TeamMaker gui instanciated.
    """
    teammaker_app = teammakergui.TeamMakerGui()
    teammaker_app.run()
