import os, shutil, subprocess

class BlendFinder:
    _viewResultsTemplate = "assets/ViewResultsTemplate.html"
    _viewResultsFilename = "BlendFinder_results.html"
    _blendExt = ".blend"
    _outputDir = "output"
    _tmpDir = "tmp"
    _outputPath = ""
    _tmpPath = ""
    blendFiles = []

    def __init__(self, filepath: str):
        self.filepath = filepath

        """create output dir"""
        self._outputPath = os.path.join(os.getcwd(), self._outputDir)

        if os.path.isdir(self._outputPath):
            shutil.rmtree(self._outputPath)
        os.mkdir(self._outputPath)

        """create temporary dir"""
        self._tmpPath = os.path.join(os.getcwd(), self._tmpDir)

        if os.path.isdir(self._tmpPath):
            shutil.rmtree(self._tmpPath)
        os.mkdir(self._tmpPath)

    def list_blend_stats(self):
        w = os.walk(self.filepath)

        for (dirpath, dirname, filenames) in w:
            for filename in filenames:
                if filename.endswith(self._blendExt):
                    self.blendFiles.append(os.path.join(dirpath, filename))

        print("There are %s .blend files." % (len(self.blendFiles)))
        print(self.blendFiles)

    def export_object(self, filename: str, index: int):
        print("Exporting %s" % (filename))
        cmd = ["blender"]
        params = ["--background", filename, "--python", "BlenderExport.py"]

        result = subprocess.run(cmd + params,
                                stdout=subprocess.PIPE)

        """create outputDir\index dir"""
        resultPath = os.path.join(".", self._outputPath, "result_" + str(index))

        if not os.path.isdir(resultPath):
            os.mkdir(resultPath)

        """copy over everything from tmp dir to result dir"""
        for outputFile in os.listdir(self._tmpPath):
            src = os.path.join(self._tmpPath, outputFile)
            dst = os.path.join(resultPath, outputFile)

            os.rename(os.path.join(self._tmpPath, outputFile),
                      os.path.join(resultPath, outputFile))

    def export_all_objects(self):
        list_items = []
        for index in range(0, len(self.blendFiles)):
            print("\nProcessing file %s out of %s: [%s]" % (index + 1, len(self.blendFiles), self.blendFiles[index]))
            self.export_object(self.blendFiles[index], index)

            list_items.append(f'<li class="item" data-item="{index}">\
                                <div class="title">{self.blendFiles[index]}</div>\
                                <img src="file:///{os.getcwd()}/output/result_{index}/render.png"/>\
                                </li>')
        with open(self._viewResultsTemplate, "r") as tpl:
            tplContent = tpl.read()

        finalContent = tplContent.replace("#CONTENT#", "\n".join(list_items))

        with open(os.path.join(self._outputPath, self._viewResultsFilename), 'w') as f:
            f.write(finalContent)
