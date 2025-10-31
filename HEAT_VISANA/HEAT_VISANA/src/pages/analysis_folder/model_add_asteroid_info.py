
from PyQt6.QtWidgets import (
  QApplication, QPushButton, QLineEdit, QFormLayout, QVBoxLayout, QHBoxLayout,
    QDialogButtonBox, QDateTimeEdit, QFrame, QStyle, QLabel, QWidget,QDialog, QGraphicsDropShadowEffect, QPlainTextEdit,
    QComboBox, QSpinBox, QDoubleSpinBox, QScrollArea
)
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator

from PyQt6.QtCore import Qt, QDateTime
from PyQt6.QtGui import  QColor
import os
import sys
import pyvista as pv
import json

module_path = 'HEAT_VISANA'
if module_path not in sys.path:
    sys.path.append(module_path)
db_path = "HEAT_VISANA/db/db.py"

if not os.path.exists(db_path):
    raise FileNotFoundError(f"Error: 'db.py' not found at {db_path}")
from db.db import DataBase
db_instance = DataBase()
from PyQt6.QtCore import pyqtSignal


class AddInfoRegionDialog(QDialog):
    saved = pyqtSignal(dict)

    def __init__(self, parent=None, mesh=None, mesh_path: str = "", created_at_qdt=None, polygons=None, download_vtk_cb=None):
        super().__init__(parent)
        self.setWindowTitle("Add Information to Database")
        self.setModal(True)
        self.setMinimumWidth(460)
        self.load_css('HEAT_VISANA/src/style/modal.css') 
        self.mesh = mesh
        self.mesh_path = mesh_path
        self.mesh_created = created_at_qdt
        self.polygons = polygons
        self.download_vtk_cb = download_vtk_cb

        # ---------- ASTEROID ----------
        asteroid_label = QLabel("ASTEROID")
        asteroid_label.setObjectName("Title")
        
        self.upload_asteroid_info = QPushButton("Load Asteroid information from Database") 
        self.upload_asteroid_info.setObjectName("Ghost") 
        self.upload_asteroid_info.setToolTip("Load asteroid details by Alt Designation or name") 
        self.upload_asteroid_info.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload))

        header_asteroid = QHBoxLayout()
        header_asteroid.addWidget(asteroid_label)
        header_asteroid.addWidget(self.upload_asteroid_info)
        header_asteroid.addStretch(1)

        asteroid_card = QFrame(); asteroid_card.setObjectName("Card")
        asteroid_card.setGraphicsEffect(self.shadow())

        self.asteroid_name = QLineEdit(placeholderText="e.g., (162173) Ryugu")
        self.alt_designation = QLineEdit(placeholderText="e.g., 1999 JU3")
        self.notes = QPlainTextEdit(); self.notes.setPlaceholderText("Short note about this asteroid")
        self.created_at = QDateTimeEdit(QDateTime.currentDateTime())
        self.created_at.setCalendarPopup(True)
        self.created_at.setDisplayFormat("yyyy-MM-dd HH:mm:ss")

        form_ast = QFormLayout()
        form_ast.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form_ast.setFormAlignment(Qt.AlignmentFlag.AlignTop)
        form_ast.setVerticalSpacing(10); form_ast.setContentsMargins(16,16,16,16)
        form_ast.addRow("Asteroid Name:", self.asteroid_name)
        form_ast.addRow("Alt Designation:", self.alt_designation)
        form_ast.addRow("Notes:", self.notes)
        form_ast.addRow("Created at:", self.created_at)
        lay_ast = QVBoxLayout(asteroid_card)
        lay_ast.setContentsMargins(12,12,12,12)
        lay_ast.addLayout(form_ast)

        # ---------- MESH ----------

        mesh_label = QLabel("Mesh"); mesh_label.setObjectName("Title")

        self.upload_mesh_info = QPushButton("Load Mesh information from Database") 
        self.upload_mesh_info.setObjectName("Ghost") 
        self.upload_mesh_info.setToolTip("Load asteroid details by Alt Designation or name") 
        self.upload_mesh_info.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload))
        header_mesh = QHBoxLayout()
        header_mesh.addWidget(mesh_label)
        header_mesh.addWidget(self.upload_mesh_info)

        header_mesh.addStretch(1)

        mesh_card = QFrame(); mesh_card.setObjectName("Card")
        mesh_card.setGraphicsEffect(self.shadow())

        self.mesh_name = QLineEdit(placeholderText="e.g., Ryugu tri-mesh v1")
        self.mesh_uri = QLineEdit(placeholderText="e.g., file:///path/model.glb")
        self.file_format = QComboBox(); self.file_format.addItems(["obj","ply","stl","glb","gltf","fbx","vtk","3ds"]); self.file_format.setEditable(True)
        self.mesh_created_at = QDateTimeEdit(QDateTime.currentDateTime()); self.mesh_created_at.setCalendarPopup(True)
        self.mesh_created_at.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.polygon_count = QSpinBox(); self.polygon_count.setRange(0, 1_000_000_000); self.polygon_count.setAccelerated(True)
        self.vertex_count  = QSpinBox(); self.vertex_count.setRange(0, 1_000_000_000); self.vertex_count.setAccelerated(True)

        # self.mesh_name = "self.ramon"
        print(f"File path: ----->", self.mesh_path[0], type(self.mesh_path[0]))
        print(f"mesh_created_at: ----->", self.mesh_created, type(self.mesh_created))
        print(f"Polygon count: ----->", self.polygon_count, type(self.polygon_count))
        

        form_mesh = QFormLayout()
        form_mesh.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form_mesh.setFormAlignment(Qt.AlignmentFlag.AlignTop)
        form_mesh.setVerticalSpacing(10); form_mesh.setContentsMargins(16,16,16,16)
        form_mesh.addRow("Mesh Name:", self.mesh_name)
        form_mesh.addRow("Mesh URI:", self.mesh_uri)
        form_mesh.addRow("Polygon Count:", self.polygon_count)
        form_mesh.addRow("Vertex Count:", self.vertex_count)
        form_mesh.addRow("Format:", self.file_format)
        form_mesh.addRow("Created at:", self.mesh_created_at)
        lay_mesh = QVBoxLayout(mesh_card); lay_mesh.setContentsMargins(12,12,12,12); lay_mesh.addLayout(form_mesh)
        
        self.mesh_name.setText("".join(self.mesh_path[0]))
        self.mesh_uri.setText("".join(self.mesh_path[0]))
        self.mesh_created_at.setDateTime(self.mesh_created)
        poly, vert = self.simple_counts(self.mesh)
        self.polygon_count.setValue(poly)
        self.vertex_count.setValue(vert)
        

        # ---------- REGION ----------
        self.region_label = QLabel("REGION"); self.region_label.setObjectName("Title")
        header_region = QHBoxLayout(); header_region.addWidget(self.region_label); header_region.addStretch(1)  # <- fixed

        region_card = QFrame(); region_card.setObjectName("Card")
        region_card.setGraphicsEffect(self.shadow())

        self.region_name = QLineEdit(placeholderText="e.g., Region of Crater Number 1")
        self.region_uri  = QLineEdit(placeholderText="e.g., file:///path/region.geojson")

        # center X/Y/Z
        

        self.region_poly_ids = QLineEdit(placeholderText="e.g., 1341, 1342, 1343")
        csv_ints_rx = QRegularExpression(r"^\s*\d+(?:\s*,\s*\d+)*\s*$")
        self.region_poly_ids.setValidator(QRegularExpressionValidator(csv_ints_rx))
        
        self.created_by = QLineEdit(placeholderText="e.g., Ramon Vilardell Bellés")
        self.region_created_at = QDateTimeEdit(QDateTime.currentDateTime()); self.region_created_at.setCalendarPopup(True)
        self.region_created_at.setDisplayFormat("yyyy-MM-dd HH:mm:ss")

        form_region = QFormLayout()
        form_region.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form_region.setFormAlignment(Qt.AlignmentFlag.AlignTop)
        form_region.setVerticalSpacing(10); form_region.setContentsMargins(16,16,16,16)
        form_region.addRow("Region Name:", self.region_name)
        form_region.addRow("Region URI:", self.region_uri)
        form_region.addRow("Region Polygon IDs:", self.region_poly_ids)
        form_region.addRow("Region Selected by:", self.created_by)
        form_region.addRow("Created at:", self.region_created_at)
        lay_region = QVBoxLayout(region_card)
        lay_region.setContentsMargins(12,12,12,12)
        lay_region.addLayout(form_region)

        self.region_name.textChanged.connect(self._sync_region_uri)


        path_str = ""
        if isinstance(self.mesh_path, (tuple, list)) and self.mesh_path:
            path_str = str(self.mesh_path[0] or "")
        elif isinstance(self.mesh_path, str):
            path_str = self.mesh_path

        self.mesh_name.setText(os.path.basename(path_str) or "")
        self.mesh_uri.setText(path_str)

        # Safe created_at
        if isinstance(self.mesh_created, QDateTime):
            self.mesh_created_at.setDateTime(self.mesh_created)

        # Counts
        if self.mesh is not None:
            poly, vert = self.simple_counts(self.mesh)
            self.polygon_count.setValue(poly)
            self.vertex_count.setValue(vert)

        # Region URI sync (you already connect the signal)
        self._sync_region_uri("")

        # DO NOT call download_vtk_cb here; do it on save.
        # Imporve robustenes
        print("HERE with polygonchan -------.>", self.polygons)
        if self.polygons:
            csv_text = ", ".join(map(str, sorted(self.polygons)))
            self.region_poly_ids.setText(csv_text)
        else:
            self.region_poly_ids.clear()

         
        #-------------------------------------#
        # ---------- SCROLL CONTENT ----------
        content = QWidget()
        content.setObjectName("ScrollContent")
        content.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        content_lay = QVBoxLayout(content); content_lay.setContentsMargins(0,0,0,0); content_lay.setSpacing(12)
        content_lay.addLayout(header_asteroid); content_lay.addWidget(asteroid_card)
        content_lay.addLayout(header_mesh);     content_lay.addWidget(mesh_card)
        content_lay.addLayout(header_region);   content_lay.addWidget(region_card)

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame) 
        scroll.viewport().setObjectName("ScrollViewport")
        scroll.viewport().setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        scroll.setWidget(content)
        scroll.setWidgetResizable(True)
        scroll.setWidget(content)

        # ---------- Buttons ----------
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Save)
        buttons.button(QDialogButtonBox.StandardButton.Save).setObjectName("Primary")
        buttons.rejected.connect(self.reject)
        buttons.accepted.connect(self.save_info)

        # ---------- Root layout (ONLY scroll + buttons) ----------
        root = QVBoxLayout(self)
        root.setContentsMargins(16,16,16,16)
        root.setSpacing(12)
        root.addWidget(scroll, 1)
        root.addWidget(buttons)

        self.resize(720, 760) 

    def save_info(self):
        # ---------- Asteroid ----------
        asteroid_name   = self.asteroid_name.text().strip()
        alt_designation = self.alt_designation.text().strip()
        notes           = self.notes.toPlainText().strip()
        created_at_ast  = self.created_at.dateTime().toUTC().toPyDateTime().replace(tzinfo=None)

        asteroid_id = db_instance.add_asteroid(asteroid_name, alt_designation, notes, created_at_ast)
        print(f"Asteroid id: {asteroid_id}")
        if not asteroid_id:
            print("Failed to insert/find asteroid; aborting mesh insert.")
            return

        # ---------- Mesh ----------
        mesh_name     = self.mesh_name.text().strip()
        mesh_uri      = self.mesh_uri.text().strip()
        file_format   = self._infer_format(mesh_uri) or self.file_format.currentText().strip().lower()
        polygon_count = int(self.polygon_count.value())
        vertex_count  = int(self.vertex_count.value())
        mesh_created  = self.mesh_created_at.dateTime().toUTC().toPyDateTime().replace(tzinfo=None)

        print("Mesh:", mesh_name, mesh_uri, polygon_count, vertex_count, file_format, mesh_created)
        mesh_id = db_instance.add_mesh(asteroid_id, mesh_name, mesh_uri, polygon_count, vertex_count, file_format, "None", mesh_created)
        print("mesh_id:", mesh_id)
        if not mesh_id:
            print("Failed to insert/find mesh; aborting region insert.")
            return

        # ---------- Region ----------
        # Keep URI in sync with name
        region_name = self.region_name.text().strip()
        self.region_uri.setText(f"Regions/{self._slug(region_name)}")
        region_uri = self._ensure_ext(self.region_uri.text().strip(), ".vtk")  # ensure .vtk

        # Polygons: use CSV of unique vertex ids for the text field
        poly_ids_text = self.region_poly_ids.text().strip()
        region_vertex_ids = [int(x) for x in poly_ids_text.split(",") if x.strip().isdigit()]

        # If you also want to store full triangles (if available), serialize to JSON
        triangles_json = None
        print("polygon------>:", self.polygons)
        if self.polygons is not None:
            try:
                arr = getattr(self.polygons, "tolist", lambda: self.polygons)()
                if arr and isinstance(arr[0], (list, tuple)):
                    triangles_json = json.dumps([[int(v) for v in tri] for tri in arr])
            except Exception:
                pass

        checksum_sha256 = "None"
        created_by = self.created_by.text().strip()
        created_at_region = self.region_created_at.dateTime().toUTC().toPyDateTime().replace(tzinfo=None)

        # IMPORTANT: if add_mesh_rigions expects plain types, serialize lists before passing
        # Here: pass poly_ids_text (CSV string) + JSON string for triangles if your schema has the column
        db_instance.add_mesh_rigions(
            asteroid_id, mesh_id, region_name, region_uri,
            poly_ids_text, json.dumps(region_vertex_ids),
            checksum_sha256, created_by, created_at_region
        )
        if callable(getattr(self, "download_vtk_cb", None)):
            try:
                self.download_vtk_cb(region_uri)  # callback must accept one arg (path)
                
            except Exception as e:
                print("download_vtk_cb failed:", e)

        self.accept()
    def as_surface(self, mesh):
        if isinstance(mesh, pv.MultiBlock):
            mesh = mesh.combine()                 # merge all blocks
        surf = mesh.extract_surface().triangulate()
        return surf

    def simple_counts(self, mesh):
        surf = self.as_surface(mesh)
        return int(surf.n_cells), int(surf.n_points) 

    def _slug(self, s: str) -> str:
        import re, unicodedata
        s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
        s = re.sub(r"[^A-Za-z0-9._-]+", "_", s).strip("_")
        return s or "unnamed"
    

    def _sync_region_uri(self, _txt: str):
        name = self.region_name.text().strip()
        self.region_uri.setText(f"Regions/{self._slug(name)}")


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

    def _infer_format(self, uri: str) -> str:
        from urllib.parse import urlparse, unquote
        p = urlparse(uri)
        path = unquote(p.path) if p.scheme else uri
        return os.path.splitext(path)[1].lstrip('.').lower()

    def _ensure_ext(self, path: str, ext: str) -> str:
        ext = ext.lstrip('.').lower()
        if not path.lower().endswith("." + ext):
            return path + "." + ext
        return path