/* OpenBRF -- by marco tarini. Provided under GNU General Public License */
/* Edited for library usage by J.SYS aka Johandros */

#include <QDebug>
#include <QApplication>
#include "mainwindow.h"
#include <QMessageBox>

using namespace std;

static void showUsage(){
  system(
    "echo off&"
    "echo off&"
    "echo.usages: &"
    "echo.&"
    "echo.  OpenBRF &"
    "echo.     ...starts GUI&"
    "echo.&"
    "echo.  OpenBRF ^<file.brf^> &"
    "echo.     ...starts GUI, opens file.brf&"
    "echo.&"
    "echo.  OpenBRF --dump ^<module_path^> ^<file.txt^>&"
    "echo.     ...shell only, dumps objects names into file.txt&"
    "echo.&"
    "echo.&"
    "pause"
  );
}


extern const char* applVersion;
static MainWindow* curWindow = nullptr;
static QApplication* curApp = nullptr;
static bool windowShown = false;


static void MainNotFoundErrorMessage()
{
    //MessageBoxA(NULL, "CUR_WINDOW_NOT_FOUND", "ERROR", MB_ICONERROR); // Windows only!!!
    QMessageBox msgBox;
    msgBox.setText("Current Windows not found!");
    msgBox.setInformativeText("Error!");
    msgBox.setIcon(QMessageBox::Critical);
    msgBox.setStandardButtons(QMessageBox::Ok);
    msgBox.setDefaultButton(QMessageBox::Ok);
    /*int ret = */msgBox.exec();
}

static bool CurWindowIsShown(bool showError = true)
{
	if (curWindow) return true;
	if (showError) MainNotFoundErrorMessage();
	return false;
}

OPENBRF_EXPORT bool IsCurHWndShown()
{
	return CurWindowIsShown(false);
}

OPENBRF_EXPORT void CloseApp()
{
	if (curApp)
		curApp->quit();
}

extern "C" int GetCurWindowPtr()
{
    //printf("%llu\n", curWindow->winId());
    return (int)curWindow->winId();
}

OPENBRF_EXPORT void SetModPath(char* modPath)
{
	if (IsCurHWndShown())
        curWindow->setModPathExternal(string(modPath));
}

OPENBRF_EXPORT void SelectIndexOfKind(int kind, int i)
{
	if (CurWindowIsShown())
		curWindow->selectTypeAndIndex(kind, i);
}

OPENBRF_EXPORT void SelectCurKindMany(int startIndex, int endIndex)
{
	if (CurWindowIsShown())
		curWindow->selectCurManyIndices(startIndex, endIndex);
}

OPENBRF_EXPORT bool SelectItemByNameAndKind(char* name, int kind = 0)
{
	if (CurWindowIsShown())
        return curWindow->searchIniExplicit(QString(name), kind);
	return false;
}

OPENBRF_EXPORT bool SelectItemByNameAndKindFromCurFile(char* name, int kind = 0)
{
    bool found = false;
	if (CurWindowIsShown())
	{
        typedef std::vector<char*> StringArray;
        StringArray names = curWindow->getMeshNames();
        string sName = string(name);
		for (size_t i = 0; i < names.size(); i++)
		{
            if (string(names[i]) == sName)
			{
				curWindow->selectTypeAndIndex(kind, (int)i);
				found = !found;
				i = names.size();
			}
		}
	}
	return found;
}

OPENBRF_EXPORT bool AddMeshToXViewModel(char* meshName, int bone = 0, int skeleton = 0, int carryPosition = -1/*, bool isAtOrigin = true*/, bool mirror = false, char* material = NULL, uint vertColor = 0)
{
    bool retur = SelectItemByNameAndKind(meshName);
	if (retur) {//includes CurWindowIsShown()
		curWindow->addLastSelectedToXViewMesh(bone, skeleton, carryPosition/*, isAtOrigin*/, mirror, material, vertColor);
	}
	return retur;
	//if (CurWindowIsShown()) {
	//	curWindow->addMeshByNameToXViewMesh(meshName, bone, skeleton, carryPosition/*, isAtOrigin*/);
	//	return true;
	//}
	//return false;
}

OPENBRF_EXPORT void ShowTroop3DPreview(bool forceUpdate = false)
{
	if (CurWindowIsShown())
		curWindow->showTroop3DPreview(forceUpdate);
}

OPENBRF_EXPORT void RemoveMeshFromXViewModel(char* meshName)
{
	//add skin name if needed here
	//if (SelectItemByNameAndKind(meshName)) {//includes CurWindowIsShown()
	//	curWindow->removeLastSelectedFromXViewMesh();
	//	return true;//maybe return remove method later (in case of error)
	//}
	//return false;
	if (CurWindowIsShown())
		curWindow->removeMeshByNameFromXViewMesh(meshName);
}

OPENBRF_EXPORT void ClearTempMeshesTroop3DPreview() {
	if (CurWindowIsShown())
		curWindow->clearTempTroop3DPreviewMeshes();
}

OPENBRF_EXPORT void AddCurSelectedMeshsAllDataToMod(char* modName) {
	if (CurWindowIsShown())
        curWindow->copyCurMeshToMod(QString(modName));
}

///////////////////////////////////////////
// FIND BETTER SOLUTION OR OPTIMIZE CODE //
// CreateSafeArrayFromBSTRArray()
// This function will create a SafeArray of BSTRs using the BSTR elements found inside
// the first parameter "pBSTRArray".
//
// Note well that the output SafeArray will contain COPIES of the original BSTRs
// inside the input parameter "pBSTRArray".
/*long CreateSafeArrayFromBSTRArray(
	BSTR* pBSTRArray,
    ulong ulArraySize,
	SAFEARRAY** ppSafeArrayReceiver
) {
	HRESULT hrRetTemp = S_OK;
	SAFEARRAY* pSAFEARRAYRet = NULL;
	SAFEARRAYBOUND rgsabound[1];
    ulong ulIndex = 0;
	long lRet = 0;

	// Initialise receiver.
	if (ppSafeArrayReceiver)
		*ppSafeArrayReceiver = NULL;

	if (pBSTRArray)
	{
		rgsabound[0].lLbound = 0;
		rgsabound[0].cElements = ulArraySize;

		pSAFEARRAYRet = (SAFEARRAY*)SafeArrayCreate
		(
			(VARTYPE)VT_BSTR,
			(unsigned int)1,
			(SAFEARRAYBOUND*)rgsabound
		);
	}

	for (ulIndex = 0; ulIndex < ulArraySize; ulIndex++)
	{
		long lIndexVector[1];

		lIndexVector[0] = ulIndex;

		// Since pSAFEARRAYRet is created as a SafeArray of VT_BSTR,
		// SafeArrayPutElement() will create a copy of each BSTR
		// inserted into the SafeArray.
		SafeArrayPutElement
		(
			(SAFEARRAY*)pSAFEARRAYRet,
			(long*)lIndexVector,
			(void*)(pBSTRArray[ulIndex])
		);
	}

	if (pSAFEARRAYRet)
		*ppSafeArrayReceiver = pSAFEARRAYRet;

	return lRet;
}*/
///////////////////////////////////////////
// FIND BETTER SOLUTION OR OPTIMIZE CODE //
//OPENBRF_EXPORT void GenerateStringsAndStoreInSafeArray(/*[out]*/ SAFEARRAY** ppSafeArrayOfStringsReceiver, char onlyCurrentModule, char commonRes)
/*{
	if (!CurWindowIsShown()) return;

    bool comRes = (commonRes > 0);

    vector<wstring> curAllNames;
    vector<vector<wstring>> allNames;

    switch ((int)onlyCurrentModule)
	{
		case 0: curWindow->getAllMeshNames(allNames, comRes); break;
		case 1:
			curWindow->getCurAllMeshNames(curAllNames, comRes);
			allNames.push_back(curAllNames);
			break;
		case 2:
			curWindow->getAllModuleNames(curAllNames);
			allNames.push_back(curAllNames);
		default: break;
	}

	uint modCount = allNames.size();
	vector<BSTR> bstrArray;//BSTR bstrArray[10] = { 0 };

	for (uint i = 0; i < modCount; i++) {
        wstring nameList;
		uint namesCount = allNames[i].size();
		for (u_int j = 0; j < namesCount; j++) {
            nameList.append(allNames[i][j]);
			nameList.append(1, (wchar_t)';');
		}
        bstrArray.push_back(::SysAllocString((BSTR)nameList.c_str()));//bstrArray[i] = ::SysAllocString(allNames[i].c_str()));
	}

	SAFEARRAY* pSafeArrayOfBSTR = NULL;
	CreateSafeArrayFromBSTRArray (
		&bstrArray[0],//vector<BSTR> to BSTR[]
		modCount,
        ppSafeArrayOfStringsReceiver
	);

	for (int i = 0; i < modCount; i++) {
        ::SysFreeString(bstrArray[i]);
	}
}*/

/**
* Main Method - For External Usage
*/
OPENBRF_EXPORT int StartExternal(int argc, char* argv[])
{
    /*bool debugMode = false;
	if (argc == 1)
		if (argv[0] == "--debug")
			debugMode = !debugMode;//true
	*/

	glClearColor(127, 127, 127, 127);//shows that there must be a bug with shaders and or material color! - if still black in gl instead of this color

	windowShown = false;

    QString nextTranslator;
	QApplication app(argc, argv);
    QStringList arguments = QCoreApplication::arguments();

	app.setApplicationVersion(applVersion);
	app.setApplicationName("OpenBrf");
	app.setOrganizationName("Marco Tarini / J.SYS");
	app.setOrganizationDomain("Marco Tarini / J.SYS");

	curApp = &app;

    bool changeModule = false;
    bool useAlphaC = false;
	if (arguments.size() > 1)
	{
		if ((arguments[1].startsWith("-")))
		{
			if ((arguments[1] == "--dump") && (arguments.size() == 4))
			{
				switch (MainWindow().loadModAndDump(arguments[2], arguments[3]))
				{
					case -1: system("echo OpenBRF: invalid module folder & pause"); break;
					case -2: system("echo OpenBRF: error scanning brf data or ini file & pause"); break;
					case -3: system("echo OpenBRF: error writing output file & pause"); break;
					default: return 0;
				}
				return -1;
			}
			else if ((arguments[1] == "--useAlphaCommands") && (arguments.size() == 2)) {
				useAlphaC = true;
				arguments.clear();
			}
			else
			{
				showUsage();
				return -1;
			}
		}
		else if (arguments.size() >= 4)
			if (arguments[2] == "-mod")
				changeModule = true;
	}

	while (1)
	{
		QTranslator translator;
		QTranslator qtTranslator;

		if (nextTranslator.isEmpty()) {
            QString loc;
			switch (MainWindow::getLanguageOption()) {
				default: loc = QLocale::system().name(); break;
                case 1: loc = QString("en"); break;
                case 2: loc = QString("zh_CN"); break;
                case 3: loc = QString("es"); break;
                case 4: loc = QString("de"); break;
			}
            translator.load(QString(":/translations/openbrf_%1.qm").arg(loc));
            qtTranslator.load(QString(":/translations/qt_%1.qm").arg(loc));
		}
		else
			translator.load(nextTranslator);

		app.installTranslator(&translator);
		app.installTranslator(&qtTranslator);

		MainWindow w;
		w.setUseAlphaCommands(useAlphaC);
		w.show();

		curWindow = &w;

		if (changeModule)
            w.setModPathExternal((char*)arguments[3].toStdString().c_str());

		if (arguments.size() > 1) 
			w.loadFile(arguments[1]);
		arguments.clear();

		windowShown = true;

		if (app.exec() == 101) {
			nextTranslator = w.getNextTranslatorFilename();
			continue;//just changed language! -> another run
		}

		windowShown = false;
		curWindow = nullptr;
		curApp = nullptr;

		break;
	}
	return 0;
}

/**
* Main Method
*/
int main(int argc, char* argv[])
{
	Q_INIT_RESOURCE(resource);
	return StartExternal(argc, argv);
}

