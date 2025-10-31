from PyQt6.QtCore import QDateTime, Qt, QRegularExpression
from PyQt6.QtWidgets import (QFileDialog,QScrollArea,QFormLayout,QDialogButtonBox,QApplication,QVBoxLayout,
                             QPushButton,QDialog,QDateTimeEdit,QDoubleSpinBox,
                             QLineEdit,QGraphicsDropShadowEffect,QSpinBox,
                             QWidget, QLabel, QHBoxLayout, QFrame, QSizePolicy, QPlainTextEdit)
from PyQt6.QtGui import QColor, QRegularExpressionValidator
from PyQt6.QtCore import pyqtSignal
import sys
import os
import json

module_path = 'HEAT_VISANA'
if module_path not in sys.path:
    sys.path.append(module_path)
db_path = "HEAT_VISANA/db/db.py"

if not os.path.exists(db_path):
    raise FileNotFoundError(f"Error: 'db.py' not found at {db_path}")
from db.db import DataBase
db_instance = DataBase()

class AddInfoCraterDialog(QDialog):
    meshSelected = pyqtSignal(str)  

    def __init__(self, parent=None, vtk_file_path: str = "", information = None):
        super().__init__(parent)

        self.vtk_file_path  = "/".join(vtk_file_path.split("/")[-2:])
        ids_region_dic = db_instance.get_info_region_from_path(self.vtk_file_path)

        self.information = information
        #print(self.information)
        
        #----- Info ------
        self.centeroid = self.information["Centroid (C)"]
        self.iniside_faces = self.information["Inside Faces"]
        self.rim_points = self.information["Boundary Points"]
        self.angle_with_horizontal_info = self.information["Angle with Horizontal"]
        self.avg_crater_slope_info = self.information["Average Crater Slope"]
        self.geodesic_diameter_info = self.information["Geodesic Diameter"]
        self.geodesic_radius_info = self.information["Geodesic Radius"]


        #----- Ids -------
        self.region_id = ids_region_dic["region_id"]
        self.asteroid_id = ids_region_dic["asteroid_id"]
        self.mesh_id = ids_region_dic["mesh_id"]

        region_id = self.region_id
        print(region_id)
        #--------------------- 

        self.setWindowTitle("Add Information to Database")
        self.setModal(True)
        self.setMinimumWidth(460)
        self.file_path = ""
        
        self.load_css('HEAT_VISANA/src/style/modal.css') 


        #------------ CRATERS -----------------
       
        header_crater, crater_card = self.create_card_crater()

        # ------------ RUN -------------
        header_run, run_card = self.create_card_run_algorithm()
        #------------- CRATER RIM -------------
        # self.create_card_crater_rim()
        header_rim, rim_card = self.create_card_crater_rim()
        
        #-------------------------------------#
        header_morf, morf_card = self.create_card_crater_morphology()
        # ---------- SCROLL CONTENT ----------

        content = QWidget()
        content.setObjectName("ScrollContent")
        content.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        content_lay = QVBoxLayout(content); content_lay.setContentsMargins(0,10,10,12); content_lay.setSpacing(12)
        content_lay.addLayout(header_crater); content_lay.addWidget(crater_card); 
        content_lay.setSpacing(12)
        content_lay.addLayout(header_run); content_lay.addWidget(run_card)
        content_lay.setSpacing(12)
        content_lay.addLayout(header_rim); content_lay.addWidget(rim_card)
        content_lay.setSpacing(12)
        content_lay.addLayout(header_morf); content_lay.addWidget(morf_card)

        # header_crater.setContentsMargins(0, 0, 0, 0)
        # header_crater.setSpacing(0)
        # crater_label.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame) 
        scroll.viewport().setObjectName("ScrollViewport")
        scroll.viewport().setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        scroll.setWidget(content)
        scroll.setWidgetResizable(True)
        scroll.setWidget(content)

        content_lay.setContentsMargins(0, 0, 0, 0)
        content_lay.setSpacing(6)
        content_lay.setAlignment(Qt.AlignmentFlag.AlignTop)


        # ---------- Buttons ----------
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Save)
        buttons.button(QDialogButtonBox.StandardButton.Save).setObjectName("Primary")
        buttons.rejected.connect(self.reject)
        buttons.accepted.connect(self.save_info)

        # ---------- Root layout (ONLY scroll + buttons) ----------
        root = QVBoxLayout(self)
        root.addWidget(scroll, 1)
        root.addWidget(buttons)

        self.resize(720, 760) 

    def create_card_crater(self):

        # ----- Header -----
        crater_label = QLabel('CRATER')
        crater_label.setObjectName("Title")
        header = QHBoxLayout()
        header.addWidget(crater_label)
        header.setContentsMargins(0, 0, 0, 0)
        header.setSpacing(0)

        # ----- Card -----
        card = QFrame()
        card.setObjectName("Card")
        eff = QGraphicsDropShadowEffect(blurRadius=18, xOffset=0, yOffset=10)
        eff.setColor(QColor(0, 0, 0, 40))
        card.setGraphicsEffect(eff)

        # ----- Fields -----
        self.crater_code = QLineEdit()
        self.crater_code.setPlaceholderText("e.g., RYUGU-001")

        self.crater_name = QLineEdit()
        self.crater_name.setPlaceholderText("e.g., Urashima, South_Ridge_A")

        self.quality_score = QDoubleSpinBox()
        self.quality_score.setRange(0.0, 1.0)
        self.quality_score.setSingleStep(0.05)
        self.quality_score.setDecimals(2)

        # future work after getting the crater itself like each rim and inside faces safe this as a vtk futur work can do Dev 
        # for practicing Qt andd PyVista to create new vtk files should not get so long to finish (I have an exemple) but 
        # try for yourself first to create there is several ways to do it but the best is do it manually because we need to 
        # mantian the same format (in my previous exemple I made there is a big mistake) when you try to create, try to find the 
        # mistake.
        # self.crater_uri = QLineEdit()
        # #self.crater_uri.setReadOnly(True)
        # self.crater_uri.setPlaceholderText("auto: Craters/<name>.vtk")

        self.crater_created_at = QDateTimeEdit(QDateTime.currentDateTime())
        self.crater_created_at.setCalendarPopup(True)
        self.crater_created_at.setDisplayFormat("yyyy-MM-dd HH:mm:ss")

        form_crater = QFormLayout()
        form_crater.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form_crater.setFormAlignment(Qt.AlignmentFlag.AlignTop)
        form_crater.setContentsMargins(16, 16, 16, 16)
        form_crater.addRow("Crater Code:", self.crater_code)
        form_crater.addRow("Crater Name:", self.crater_name)
        form_crater.addRow("Quality Score:", self.quality_score)
        # form_crater.addRow("Crater URI:", self.crater_uri)
        form_crater.addRow("Created at:", self.crater_created_at)
     
        crater_card_layout = QVBoxLayout(card)
        crater_card_layout.addLayout(form_crater)
    
        return header, card
    
    def create_card_crater_rim(self):

        # ----- Header -----
        rim_label = QLabel("CRATER RIM INFO")
        rim_label.setObjectName("Title")
        header = QHBoxLayout()
        header.addWidget(rim_label)
        header.setContentsMargins(0, 0, 0, 0)
        header.setSpacing(0)

        # ----- Card -----
        card = QFrame()
        card.setObjectName("Card")
        eff = QGraphicsDropShadowEffect(blurRadius=18, xOffset=0, yOffset=10)
        eff.setColor(QColor(0, 0, 0, 40))
        card.setGraphicsEffect(eff)

        # ----- Fields -----

        self.rim_area = QDoubleSpinBox()
        self.rim_area.setDecimals(6)
        self.rim_area.setRange(0.0, 1e18)
        self.rim_area.setSingleStep(0.1)
        self.rim_area.setSuffix(" m²")
        self.rim_area.setToolTip("Cached area in your units")

        self.vertices_count = QSpinBox()
        self.vertices_count.setRange(0, 1_000_000_000)
        self.vertices_count.setAccelerated(True)
        self.vertices_count.setToolTip("ST_NPoints equivalent (cached)")

        # Center as XYZ + derived WKT POINT Z
        self.center_x = QDoubleSpinBox(); self.center_y = QDoubleSpinBox(); self.center_z = QDoubleSpinBox()
        for sb in (self.center_x, self.center_y, self.center_z):
            sb.setDecimals(6); sb.setSingleStep(0.1); sb.setRange(-1e12, 1e12); sb.setMinimumWidth(110)
        center_row = QWidget()
        center_lay = QHBoxLayout(center_row); center_lay.setContentsMargins(0,0,0,0); center_lay.setSpacing(8)
        center_lay.addWidget(QLabel("X")); center_lay.addWidget(self.center_x)
        center_lay.addWidget(QLabel("Y")); center_lay.addWidget(self.center_y)
        center_lay.addWidget(QLabel("Z")); center_lay.addWidget(self.center_z)
        center_lay.addStretch(1)

        # def _sync_center_wkt():
        #     x, y, z = self.center_x.value(), self.center_y.value(), self.center_z.value()
        #     self.rim_center_wkt.setText(f"POINT Z ({x:.6f} {y:.6f} {z:.6f})")
        # for sb in (self.center_x, self.center_y, self.center_z):
        #     sb.valueChanged.connect(_sync_center_wkt)
        # _sync_center_wkt()

        # Polygon IDs as CSV (JSON is built when saving)
        self.rim_polygon_ids = QLineEdit(placeholderText="e.g., 1341, 1342, 1343")
        csv_ints_rx = QRegularExpression(r"^\s*\d+(?:\s*,\s*\d+)*\s*$")
        self.rim_polygon_ids.setValidator(QRegularExpressionValidator(csv_ints_rx))
        self.rim_polygon_ids.setToolTip("Comma-separated list of face/vertex IDs")

        # Created at
        self.rim_created_at = QDateTimeEdit(QDateTime.currentDateTime())
        self.rim_created_at.setCalendarPopup(True)
        self.rim_created_at.setDisplayFormat("yyyy-MM-dd HH:mm:ss")

        # ----- Layout inside card -----
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form.setFormAlignment(Qt.AlignmentFlag.AlignTop)
        form.setContentsMargins(16, 16, 16, 16)

        form.addRow("Rim Area:", self.rim_area)
        form.addRow("Rim Center (XYZ):", center_row)
        form.addRow("Vertices Count:", self.vertices_count)
        form.addRow("Rim Boundary Points:", self.rim_polygon_ids)
        form.addRow("Created at:", self.rim_created_at)

        self.rim_area.setValue(self.information["rim_area"])

        self.vertices_count.setValue(self.information["vertices_count"])
        
        poly = self.information["rim_polygon_ids"]

        if poly:
            csv_text = ", ".join(map(str, sorted(poly)))
            self.rim_polygon_ids.setText(csv_text)
        else:
            self.rim_polygon_ids.clear()
        
        self.center_x.setValue(self.information["rim_center"][0])
        self.center_y.setValue(self.information["rim_center"][1])
        self.center_z.setValue(self.information["rim_center"][2])
        
        
        # results["circularity"]  =  circularity
        # results["dimater_equivelent"] = D_eq

        card_lay = QVBoxLayout(card)
        card_lay.addLayout(form)

        return header, card

    def create_card_crater_morphology(self):
        # ----- Header -----
        morf_label = QLabel("CRATER RIM MORPHOLOGY")
        morf_label.setObjectName("Title")
        header = QHBoxLayout()
        header.addWidget(morf_label)
        header.setContentsMargins(0, 0, 0, 0)
        header.setSpacing(0)

        # ----- Card -----
        card = QFrame()
        card.setObjectName("Card")
        eff = QGraphicsDropShadowEffect(blurRadius=18, xOffset=0, yOffset=10)
        eff.setColor(QColor(0, 0, 0, 40))
        card.setGraphicsEffect(eff)

        # ----- Fields -----


        self.depth_c = QDoubleSpinBox()
        self.depth_c.setDecimals(6)
        self.depth_c.setRange(0.0, 1e18)
        self.depth_c.setSingleStep(0.1)
        self.depth_c.setSuffix(" m²")
        self.depth_c.setToolTip("Cached area in your units")

        self.angle_with_horizontal = QDoubleSpinBox()
        self.angle_with_horizontal.setDecimals(4)
        self.angle_with_horizontal.setRange(0.0, 1e18)
        self.angle_with_horizontal.setSingleStep(0.1)
        self.angle_with_horizontal.setSuffix("°")

        self.avg_crater_slope = QDoubleSpinBox()
        self.avg_crater_slope.setDecimals(4)
        self.avg_crater_slope.setRange(0.0, 1e18)
        self.avg_crater_slope.setSingleStep(0.1)
        self.avg_crater_slope.setSuffix("°")
        
        self.geodesic_diameter = QDoubleSpinBox()
        self.geodesic_diameter.setDecimals(6)
        self.geodesic_diameter.setRange(0.0, 1e18)
        self.geodesic_diameter.setSingleStep(0.1)
        self.geodesic_diameter.setSuffix(" m²")
        self.geodesic_diameter.setToolTip("Cached area in your units")

        self.geodesic_radius = QDoubleSpinBox()
        self.geodesic_radius.setDecimals(6)
        self.geodesic_radius.setRange(0.0, 1e18)
        self.geodesic_radius.setSingleStep(0.1)
        self.geodesic_radius.setSuffix(" m²")
        self.geodesic_radius.setToolTip("Cached area in your units")

        self.centroid_x = QDoubleSpinBox(); self.centroid_y = QDoubleSpinBox(); self.centroid_z = QDoubleSpinBox()
        for sb in (self.centroid_x, self.centroid_y, self.centroid_z):
            sb.setDecimals(6); sb.setSingleStep(0.1); sb.setRange(-1e12, 1e12); sb.setMinimumWidth(110)
        centroid_row = QWidget()
        centroid_lay = QHBoxLayout(centroid_row); centroid_lay.setContentsMargins(0,0,0,0); centroid_lay.setSpacing(8)
        centroid_lay.addWidget(QLabel("X")); centroid_lay.addWidget(self.centroid_x)
        centroid_lay.addWidget(QLabel("Y")); centroid_lay.addWidget(self.centroid_y)
        centroid_lay.addWidget(QLabel("Z")); centroid_lay.addWidget(self.centroid_z)
        centroid_lay.addStretch(1)

        self.crater_diameter = QDoubleSpinBox()
        self.crater_diameter.setDecimals(6)
        self.crater_diameter.setRange(0.0, 1e18)
        self.crater_diameter.setSingleStep(0.1)
        self.crater_diameter.setSuffix(" m²")
        self.crater_diameter.setToolTip("Cached area in your units")

        
        self.units = QLineEdit()
        self.units.setPlaceholderText("e.g., m²")
        
        # ----- Layout inside card -----
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form.setFormAlignment(Qt.AlignmentFlag.AlignTop)
        form.setContentsMargins(16, 16, 16, 16)

        form.addRow("Crater Depth:", self.depth_c)
        form.addRow("Crater Angle With Horizontal:", self.angle_with_horizontal)
        form.addRow("Avarage Crater Slope:", self.avg_crater_slope) #this should be reculated after smoothing laplacian
        form.addRow("Crater Geodestic Diamter:", self.geodesic_diameter)
        form.addRow("Crater Geodestic Radius:", self.geodesic_radius)
        form.addRow("Crater Centeroid (XYZ):", centroid_row)
        form.addRow("Crater Diamter:", self.crater_diameter)
        form.addRow("Units:", self.units)

    

        ["Diameter Endpoints"]
        ['Crater Diameter from the Circle']

        self.depth_c.setValue(self.information["Depth"]*1000.0)
        self.angle_with_horizontal.setValue(self.information["Angle with Horizontal"])
        self.avg_crater_slope.setValue(self.information["Average Crater Slope"])
        self.geodesic_diameter.setValue(self.information["Geodesic Diameter"])
        self.geodesic_radius.setValue(self.information["Geodesic Radius"])
        self.centroid_x.setValue(self.information["Centroid (C)"][0])
        self.centroid_y.setValue(self.information["Centroid (C)"][1])
        self.centroid_z.setValue(self.information["Centroid (C)"][2])
        self.units.setText("m^2")

        card_lay = QVBoxLayout(card)
        card_lay.addLayout(form)
         
        return header, card

    def create_card_run_algorithm(self):
        # ----- Header -----
        run_label = QLabel('RUN ALGORITHM INFO')
        run_label.setObjectName("Title")
        header = QHBoxLayout()
        header.addWidget(run_label)
        header.setContentsMargins(0, 0, 0, 0)
        header.setSpacing(0)

        # ------- CARD -----
        card = QFrame()
        card.setObjectName("Card")
        eff = QGraphicsDropShadowEffect(blurRadius=18, xOffset=0, yOffset=10)
        eff.setColor(QColor(0, 0, 0, 40))
        card.setGraphicsEffect(eff)

        #----- FIELDS -------
        self.method_name = QLineEdit(); self.method_name.setPlaceholderText("APBT_v1")
        
        self.method_version = QLineEdit(); self.method_version.setPlaceholderText("v1")

        self.parameters = QPlainTextEdit(); self.parameters.setPlaceholderText("0.5µ on smoothing paraments...")

        self.executed_by = QLineEdit(placeholderText="e.g., Ramon Vilardell Bellés")
        self.executed_at = QDateTimeEdit(QDateTime.currentDateTime()); self.executed_at.setCalendarPopup(True)

        self.notes = QPlainTextEdit(); self.notes.setPlaceholderText("This time fail in the North...")

        form_run = QFormLayout()
        form_run.setLabelAlignment(Qt.AlignmentFlag.AlignTop)
        form_run.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form_run.setContentsMargins(16, 16, 16, 16)
        form_run.addRow("Method Name:",self.method_name); form_run.addRow("Method Version:", self.method_version)
        form_run.addRow("Parameters:", self.parameters); form_run.addRow("Executed By:", self.executed_by)
        form_run.addRow("Exectuted At:", self.executed_at); form_run.addRow("Notes:", self.notes)

        run_card_layout = QVBoxLayout(card)
        run_card_layout.addLayout(form_run)

        return header, card
        #run_id, asteroid_id, mesh_id, method_name, method_version, parameters, executed_by, executed_at, notes

    def save_info(self):

        asteroid_id = self.asteroid_id
        mesh_id = self.mesh_id
        region_id = self.region_id
        print(region_id)
        method_name = self.method_name.text().strip(); method_version = self.method_version.text().strip()
        parameters = self.parameters.toPlainText().strip(); executed_by = self.executed_by.text().strip(); 
        executed_at = self.executed_at.dateTime().toUTC().toPyDateTime().replace(tzinfo=None)
        notes = self.notes.toPlainText().strip()
        if not parameters:
            parameters_json = json.dumps({})
        else:
            parameters_json = json.dumps({"text:":parameters})

        run_id = db_instance.add_run_info(asteroid_id, mesh_id,region_id, method_name, method_version, parameters_json, executed_by, executed_at, notes)
      
        print("run_id: ",run_id)
        crater_code   = self.crater_code.text().strip()
        crater_name = self.crater_name.text().strip()
        quality_score           = float(self.quality_score.value()) 
        created_at  = self.crater_created_at.dateTime().toUTC().toPyDateTime().replace(tzinfo=None)
        crater_uri = self.file_path
        crater_id =  db_instance.add_craters( asteroid_id, run_id,region_id, crater_code, crater_name, quality_score, crater_uri, created_at)
        print("crater_id",crater_id)

        # rim_center = ",".join([str(self.center_x.value()), str(self.center_y.value()), str(self.center_z.value())])
        # rim_center_json = json.dumps({"x": self.center_x,
        #                       "y": self.center_y,
        #                       "z": self.center_z})
        rim_center = json.dumps({  
                "x": float(self.center_x.value()),
                "y": float(self.center_y.value()),
                "z": float(self.center_z.value()),
            })
        rim_geom = None
        rim_area = float(self.rim_area.value())
        vertices_count = self.vertices_count.value()
        rim_polygon_ids  = self.rim_polygon_ids.text().strip()
        #rim_polygon_ids = [int(x) for x in rim_polygon_ids.split(",") if x.strip().isdigit()]
        seed_points = ",".join(str(point) for point in self.information["Seed Points"])
        #print("Seed Points: ", seed_points)
        created_at_cr = self.rim_created_at.dateTime().toUTC().toPyDateTime().replace(tzinfo=None)
        db_instance.add_crater_rims(crater_id, mesh_id, rim_center, rim_area, vertices_count, rim_polygon_ids, created_at_cr, seed_points)


        depth = float(self.depth_c.value())
        angle_with_horizontal = float(self.angle_with_horizontal.value())
        avg_crater_slope = float(self.avg_crater_slope.value())
        geodesic_diameter = float(self.geodesic_diameter.value())
        geodesic_radius = float(self.geodesic_radius.value())

        centroid_x = float(self.centroid_x.value())
        centroid_y = float(self.centroid_y.value())
        centroid_z = float(self.centroid_z.value())  

        crater_diameter = 0.0
        units = self.units.text().strip()

        db_instance.add_crater_morphology(
            crater_id, depth, angle_with_horizontal, avg_crater_slope,
            geodesic_diameter, geodesic_radius, centroid_x, centroid_y, centroid_z,
            crater_diameter, units
        )
        self.accept()

    def shadow(self):
        shadow = QGraphicsDropShadowEffect(blurRadius=18, xOffset=0, yOffset=10)
        shadow.setColor(QColor(0, 0, 0, 40))
        return shadow

    def load_css(self, file_path):
        try:
            with open(file_path, 'r') as css_file:
                css = css_file.read()
                self.setStyleSheet(css)
        except FileNotFoundError:
            print(f"Error: The file {file_path} was not found.")
        except Exception as e:
            print(f"Error loading CSS: {e}")

