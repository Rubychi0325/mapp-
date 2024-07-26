<template>
  <div class="container">
    <div class="main-content">
      <div class="canvas-container">
        <canvas ref="canvas" width="1000" height="700" 
                @click="handleCanvasClick"
                @mousemove="handleMouseMove"
                @mouseup="handleMouseUp"
                @mousedown="handleImageMouseDown"
                @wheel="handleWheel">
          Your browser does not support the HTML5 canvas tag.
        </canvas>
      </div>

      <div class="export-import-buttons">
        <button @click="exportCSV">匯出</button>
        <button @click="importCSV">匯入</button>
        <input type="file" ref="fileInput" style="display: none;" @change="handleFileUpload">
      </div>

      <div class="mode-selection">
        <button :class="{ active: currentMode === 'drawPoint' }" @click="setCurrentMode('drawPoint')">點</button>
        <button :class="{ active: currentMode === 'drawPath' }" @click="setCurrentMode('drawPath')">路徑</button>
        <button :class="{ active: currentMode === 'clickMode' }" @click="setCurrentMode('clickMode')">點選</button>
      </div>
    </div>

    <div v-if="showPopup" class="popup">
      <div v-if="currentMode === 'drawPoint' && addingPoint">
        <table class="info-table">
          <tr>
            <td colspan="2">新增點</td>
          </tr>
          <tr>
            <td><label for="tag-id">Tag_ID</label></td>
            <td><input type="text" id="tag-id" v-model="newPoint.tagID"></td>
          </tr>
          <tr>
            <td><label for="tag-name">Tag_Name</label></td>
            <td><input type="text" id="tag-name" v-model="newPoint.tagName"></td>
          </tr>
          <tr>
            <td><label for="x-coordinate">X 座標</label></td>
            <td><input type="number" id="x-coordinate" v-model.number="newPoint.x"></td>
          </tr>
          <tr>
            <td><label for="y-coordinate">Y 座標</label></td>
            <td><input type="number" id="y-coordinate" v-model.number="newPoint.y"></td>
          </tr>
          <tr>
            <td><label for="floor">樓層</label></td>
            <td><input type="text" id="floor" v-model="newPoint.floor"></td>
          </tr>
          <tr>
            <td><label for="floorid">樓層編號</label></td>
            <td><input type="text" id="floorid" v-model="newPoint.floorid"></td>
          </tr>
          <tr>
            <td colspan="2">
              <button class="table-btn btn btn-delete" @click="cancelAddPoint">取消</button>
              <button class="table-btn" @click="confirmAddPoint">確認新增</button>
            </td>
          </tr>
        </table>
      </div>

      <div v-if="currentMode === 'drawPath' && pathPoints.length === 2">
        <table class="info-table">
          <tr>
            <td colspan="2">新增路徑</td>
          </tr>
          <tr>
            <td><strong>起點Tag_ID</strong></td>
            <td>{{ pathPoints[0].tagID }}</td>
          </tr>
          <tr>
            <td><strong>起點坐標</strong></td>
            <td>({{ pathPoints[0].x }}, {{ pathPoints[0].y }})</td>
          </tr>
          <tr>
            <td><strong>終點Tag_ID</strong></td>
            <td>{{ pathPoints[1].tagID }}</td>
          </tr>
          <tr>
            <td><strong>終點坐標</strong></td>
            <td>({{ pathPoints[1].x }}, {{ pathPoints[1].y }})</td>
          </tr>
          <tr>
            <td><label for="path-speed">路徑速度</label></td>
            <td><input type="number" id="path-speed" v-model.number="newPath.speed" min="0" step="0.1"></td>
          </tr>
          <tr>
            <td colspan="2">
              <button class="table-btn btn btn-delete" @click="cancelAddPath">取消</button>
              <button class="table-btn" @click="confirmAddPath">確認新增</button>
            </td>
          </tr>
        </table>
      </div>

      <div v-if="selectedPoint || selectedPath">
        <div v-if="selectedPoint">
          <table class="info-table">
            <tr>
              <td colspan="2">點資訊</td>
            </tr>
            <tr>
              <td><strong>Tag_ID</strong></td>
              <td><input type="text" v-model="selectedPoint.tagID" :disabled="!isEditingPoint"></td>
            </tr>
            <tr>
              <td><strong>X 座標</strong></td>
              <td><input type="number" v-model.number="selectedPoint.x" :disabled="!isEditingPoint"></td>
            </tr>
            <tr>
              <td><strong>Y 座標</strong></td>
              <td><input type="number" v-model.number="selectedPoint.y" :disabled="!isEditingPoint"></td>
            </tr>
            <tr>
              <td><strong>樓層</strong></td>
              <td><input type="text" v-model="selectedPoint.floor" :disabled="!isEditingPoint"></td>
            </tr>
            <tr>
              <td><strong>樓層編號</strong></td>
              <td><input type="number" v-model="selectedPoint.floorid" :disabled="!isEditingPoint"></td>
            </tr>
            <tr>
              <td colspan="2">
                <button class="table-btn btn-cancel" @click="cancelPointEdit(selectedPoint)" v-if="isEditingPoint">取消修改</button>
                <button class="table-btn btn-update" @click="confirmPointEdit" v-if="isEditingPoint">確認修改</button>
                <button class="table-btn btn-update" @click="enablePointEdit(selectedPoint)" v-if="!isEditingPoint">修改點</button>
                <button class="table-btn btn-delete" @click="deletePoint(selectedPoint)">刪除點</button>
              </td>
            </tr>
          </table>

          <ul v-if="selectedPoint">
            <li v-for="path in getRelatedPaths(selectedPoint)" :key="`${path.start.tagID}-${path.end.tagID}`">
              <table class="info-table">
                <tr>
                  <td colspan="2">路徑資訊</td>
                </tr>
                <tr>
                  <td><strong>起點 Tag_ID</strong></td>
                  <td>{{ path.start.tagID }}</td>
                </tr>
                <tr>
                  <td><strong>終點 Tag_ID</strong></td>
                  <td>{{ path.end.tagID }}</td>
                </tr>
                <tr>
                  <td><strong>起點坐標</strong></td>
                  <td>({{ path.start.x }}, {{ path.start.y }})</td>
                </tr>
                <tr>
                  <td><strong>終點坐標</strong></td>
                  <td>({{ path.end.x }}, {{ path.end.y }})</td>
                </tr>
                <tr>
                  <td><strong>路徑速度</strong></td>
                  <td><input type="number" v-model.number="path.speed" :disabled="!isEditingPath"></td>
                </tr>
                <tr>
                  <td colspan="2">
                    <button class="table-btn btn btn-cancel" @click="cancelPathEdit" v-if="isEditingPath">取消修改</button>
                    <button class="table-btn btn btn-update" @click="confirmPathEdit" v-if="isEditingPath">確認修改</button>
                    <button class="table-btn btn btn-update" @click="enablePathEdit(path)" v-if="!isEditingPath">修改路徑</button>
                    <button class="table-btn btn btn-delete" @click="deletePath(path)">刪除路徑</button>
                  </td>
                </tr>
              </table>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <div v-if="isConfirmingDelete" class="confirmation-dialog">
      <p>{{ deleteType === 'point' ? '是否要刪除此點？ (相關路徑也會跟著刪除喔！)' : '是否要刪除此路徑？' }}</p>
      <button @click="confirmDelete">確認</button>
      <button @click="cancelDelete">取消</button>
    </div>
    <div v-if="isConfirmingPointEdit" class="confirmation-dialog">
      <p>是否要將點移動到新位置？</p>
      <button @click="confirmPointMove">確認</button>
      <button @click="cancelPointMove">取消</button>
    </div>
  </div>
</template>

<script>
import mapImage from '@/assets/MAP1F1.png';
import { saveAs } from 'file-saver';

export default {
  name: 'MapFunction',
  data() {
    return {
      context: null,
      currentMode: 'drawPoint',
      points: [],
      selectedPoint: null,
      addingPoint: false,
      defaultTagID: '',
      newPoint: {
        x: 0,
        y: 0,
        tagID: '',
        tagName: '',
        floor: '',
        floorid: ''
      },
      pathPoints: [],
      newPath: {
        endX: 0,
        endY: 0,
        speed: 0
      },
      paths: [],
      selectedPath: null,
      isEditingPoint: false,
      isEditingPath: false,
      originalPoint: {},
      originalPath: {},
      
      isDragging: false,
      dragPoint: null,

      image: null,
      imageX: 0,
      imageY: 0,
      dragOffsetX: 0,
      dragOffsetY: 0,
      scale: 1,
      imageScale: 1,
      imageOffsetX: 0,
      imageOffsetY: 0,
      isDraggingImage: false,
      lastMouseX: 0,
      lastMouseY: 0,
      isConfirmingPointEdit: false,
      tempPoint: null,
      isConfirmingDelete: false,
      deleteTarget: null,
      deleteType: '',
      showPopup: false,
    };
  },
  mounted() {
    this.context = this.$refs.canvas.getContext('2d');
    this.loadImage();
    this.defaultTagID = this.getNextTagID();

    this.$refs.canvas.width = window.innerWidth * 0.8;  // 例如，設置為窗口寬度的80%
    this.$refs.canvas.height = window.innerHeight * 0.8;  // 設置為窗口高度的80%

    window.addEventListener('resize', this.handleResize);
  },
  methods: {
    loadImage() {
      this.image = new Image();
      this.image.src = mapImage;
      this.image.onload = () => {
        this.imageX = (this.$refs.canvas.width - this.image.width) / 2;
        this.imageY = (this.$refs.canvas.height - this.image.height) / 2;
        this.drawImage();
      };
    },
    drawImage() {
      if (this.image) {
        const scaledWidth = this.image.width * this.imageScale;
        const scaledHeight = this.image.height * this.imageScale;
        this.context.drawImage(
          this.image,
          this.imageOffsetX,
          this.imageOffsetY,
          scaledWidth,
          scaledHeight
        );
      }
    },
    setCurrentMode(mode) {
      this.currentMode = mode;
      if (mode !== 'drawPath') {
        this.clearPathPreview();
      }
      this.showPopup = false;
    },
    handleCanvasClick(event) {
      const mouseX = Number(((event.offsetX - this.imageOffsetX) / this.imageScale).toFixed(1));
      const mouseY = Number(((event.offsetY - this.imageOffsetY) / this.imageScale).toFixed(1));

      if (this.addingPoint) {
        this.clearCanvas();
        this.redrawPoints();
        this.redrawPaths();
      }

      if (this.isEditingPoint && this.selectedPoint) {
        this.isDragging = true;
        this.dragPoint = this.selectedPoint;
      } else if (this.currentMode === 'drawPoint') {
        this.addingPoint = true;
        this.newPoint.x = mouseX;
        this.newPoint.y = mouseY;
        this.drawPoint(mouseX, mouseY, 'red');
        this.showPopup = true;
      } else if (this.currentMode === 'clickMode') {
        this.showPointInfo(mouseX, mouseY);
      } else if (this.currentMode === 'drawPath') {
        this.addPathPoint(mouseX, mouseY);
      }
    },
    getNextTagID() {
      if (this.points.length === 0) {
        return '0001';
      } else {
        const maxID = Math.max(...this.points.map(point => parseInt(point.tagID)));
        return (maxID + 1).toString().padStart(4, '0');
      }
    },
    confirmAddPoint() {
      if (this.newPoint.tagID === '' || this.newPoint.tagName === '' || this.newPoint.x === 0 || this.newPoint.y === 0|| this.newPoint.floor === ''|| this.newPoint.floorid === '') {
        alert('請填寫所有必填欄位！');
        return;
      }
    
      this.points.push({
        x: this.newPoint.x,
        y: this.newPoint.y,
        tagID: this.newPoint.tagID,
        tagName: this.newPoint.tagName,
        floor: this.newPoint.floor,
        floorid: this.newPoint.floorid
      });

      this.drawPoint(this.newPoint.x, this.newPoint.y);
      this.resetNewPoint();
    },
    cancelAddPoint() {
      this.resetNewPoint();
      this.clearCanvas();
      this.redrawPoints();
      this.redrawPaths();
    },
    resetNewPoint() {
      const nextTagID = this.getNextTagID();
      this.newPoint.x = 0;
      this.newPoint.y = 0;
      this.newPoint.tagID = nextTagID;
      this.newPoint.tagName = nextTagID;
      this.newPoint.floor = '';
      this.newPoint.floorid = '';
      this.addingPoint = false;
      this.showPopup = false;
    },
    drawPoint(x, y, color = 'blue') {
      const canvasX = this.imageOffsetX + x * this.imageScale;
      const canvasY = this.imageOffsetY + y * this.imageScale;
      this.context.beginPath();
      this.context.arc(canvasX, canvasY, 6, 0, Math.PI * 2);
      this.context.fillStyle = color;
      this.context.fill();
      this.context.strokeStyle = 'white';
      this.context.lineWidth = 2;
      this.context.stroke();

      const tagID = this.points.find(point => point.x === x && point.y === y)?.tagID;
      if (tagID) {
        this.context.font = '12px Arial';
        this.context.fillStyle = 'white';
        this.context.strokeStyle = 'black';
        this.context.lineWidth = 3;
        this.context.strokeText(`${tagID}`, canvasX + 10, canvasY - 10);
        this.context.fillText(`${tagID}`, canvasX + 10, canvasY - 10);
      }
    },
    addPathPoint(mouseX, mouseY) {
      let clickedPoint = null;
      for (const point of this.points) {
        if (Math.abs(point.x - mouseX) <= 3 / this.imageScale && Math.abs(point.y - mouseY) <= 3 / this.imageScale) {
          clickedPoint = point;
          break;
        }
      }
      if (clickedPoint) {
        this.pathPoints.push({ 
          x: Number(clickedPoint.x.toFixed(1)), 
          y: Number(clickedPoint.y.toFixed(1)), 
          tagID: clickedPoint.tagID 
        });
        if (this.pathPoints.length === 2) {
          const startPoint = this.pathPoints[0];
          const endPoint = this.pathPoints[1];
        
          this.newPath.endX = endPoint.x;
          this.newPath.endY = endPoint.y;
        
          this.drawDashedLine(startPoint.x, startPoint.y, endPoint.x, endPoint.y);
          this.showPopup = true;
        }
      }
    },
    confirmAddPath() {
      const startPoint = this.pathPoints[0];
      const endPoint = this.pathPoints[1];
      const path = {
        start: startPoint,
        end: endPoint,
        speed: this.newPath.speed
      };
    
      this.paths.push(path);
    
      this.clearPathPreview();
      this.pathPoints = [];
    
      this.clearCanvas();
      this.redrawPoints();
      this.redrawPaths();
      this.showPopup = false;
      },
      cancelAddPath() {
      this.clearPathPreview();
      this.pathPoints = [];
      this.showPopup = false;
      },
      clearPathPreview() {
      this.clearCanvas();
      this.redrawPoints();
      this.redrawPaths();
      },
      drawDashedLine(x1, y1, x2, y2) {
      const canvasX1 = this.imageOffsetX + x1 * this.imageScale;
      const canvasY1 = this.imageOffsetY + y1 * this.imageScale;
      const canvasX2 = this.imageOffsetX + x2 * this.imageScale;
      const canvasY2 = this.imageOffsetY + y2 * this.imageScale;
      
      this.context.beginPath();
      this.context.setLineDash([5, 5]);
      this.context.moveTo(canvasX1, canvasY1);
      this.context.lineTo(canvasX2, canvasY2);
      this.context.strokeStyle = 'gray';
      this.context.stroke();
      this.context.setLineDash([]);
    },
    showPointInfo(mouseX, mouseY) {
      for (const point of this.points) {
        if (Math.abs(point.x - mouseX) <= 3 && Math.abs(point.y - mouseY) <= 3) {
          this.selectedPoint = {
            ...point,
            x: Number(point.x.toFixed(1)),
            y: Number(point.y.toFixed(1))
          };
          this.selectedPath = null; 
          this.clearCanvas();
          this.redrawPoints();
          this.redrawPaths();
          this.drawPoint(point.x, point.y, 'green');
          this.showPopup = true;
          return;
        }
      }
      this.selectedPoint = null;
      this.selectedPath = null;
      this.showPopup = false;
    },
    getRelatedPaths(point) {
      return this.paths.filter(path => 
        path.start.x === point.x && path.start.y === point.y
      );
    },
    deletePoint(pointToDelete) {
      this.isConfirmingDelete = true;
      this.deleteTarget = pointToDelete;
      this.deleteType = 'point';
    },
    deletePath(pathToDelete) {
      this.isConfirmingDelete = true;
      this.deleteTarget = pathToDelete;
      this.deleteType = 'path';
    },
    clearCanvas() {
      this.context.clearRect(0, 0, this.$refs.canvas.width, this.$refs.canvas.height);
      this.drawImage();
    },
    redrawPoints() {
      for (const point of this.points) {
        this.drawPoint(point.x, point.y);
      }
    },
    redrawPaths() {
      this.context.beginPath();
      this.context.strokeStyle = 'black';
      this.context.lineWidth = 1;
      
      for (const path of this.paths) {
        this.drawLine(path.start.x, path.start.y, path.end.x, path.end.y);
      }
    },
    drawLine(x1, y1, x2, y2) {
      const canvasX1 = this.imageOffsetX + x1 * this.imageScale;
      const canvasY1 = this.imageOffsetY + y1 * this.imageScale;
      const canvasX2 = this.imageOffsetX + x2 * this.imageScale;
      const canvasY2 = this.imageOffsetY + y2 * this.imageScale;
      
      this.context.beginPath();
      this.context.moveTo(canvasX1, canvasY1);
      this.context.lineTo(canvasX2, canvasY2);
      this.context.stroke();
    },
    enablePointEdit(point) {
      if (this.isEditingPoint) {
          this.confirmPointEdit();
      }
      this.isEditingPoint = true;
      this.originalPoint = { ...point };
    },
    confirmPointEdit() {
      const index = this.points.findIndex(p => p.x === this.selectedPoint.x && p.y === this.selectedPoint.y);
      if (index !== -1) {
        this.points[index] = { ...this.selectedPoint };
      
        for (const path of this.paths) {
          if (path.start.x === this.originalPoint.x && path.start.y === this.originalPoint.y) {
            path.start = { ...this.selectedPoint };
          }
          if (path.end.x === this.originalPoint.x && path.end.y === this.originalPoint.y) {
            path.end = { ...this.selectedPoint };
          }
        }
      }
      this.isEditingPoint = false;
      this.dragPoint = null;
      this.originalPoint = {};

      this.clearCanvas();
      this.redrawPoints();
      this.redrawPaths();
    },
    cancelPointEdit(point) {
      const index = this.points.findIndex(p => p.x === point.x && p.y === point.y);
      if (index !== -1) {
        this.points[index].x = this.originalPoint.x;
        this.points[index].y = this.originalPoint.y;
        this.points[index].tagID = this.originalPoint.tagID;
        this.points[index].tagName = this.originalPoint.tagName;
      }
      this.isEditingPoint = false;
      this.originalPoint = {};

      this.clearCanvas();
      this.redrawPoints();
      this.redrawPaths();
    },
    enablePathEdit(path) {
      this.isEditingPath = true;
      this.originalPath = { ...path };
      this.selectedPath = path;
    },
    confirmPathEdit() {
      const index = this.paths.findIndex(p => p.start.x === this.selectedPath.start.x && p.start.y === this.selectedPath.start.y && p.end.x === this.selectedPath.end.x && p.end.y === this.selectedPath.end.y);
      if (index !== -1) {
        this.paths[index].speed = this.selectedPath.speed;
      }

      this.isEditingPath = false;
      this.originalPath = {};

      this.clearCanvas();
      this.redrawPoints();
      this.redrawPaths();
    },
    cancelPathEdit() {
      const index = this.paths.findIndex(p => p.start.x === this.originalPath.start.x && p.start.y === this.originalPath.start.y && p.end.x === this.originalPath.end.x && p.end.y === this.originalPath.end.y);
      if (index !== -1) {
        this.paths[index].speed = this.originalPath.speed;
      }

      this.isEditingPath = false;
      this.originalPath = {};

      this.clearCanvas();
      this.redrawPoints();
      this.redrawPaths();
    },
    handleImageMouseDown(event) {
      if (this.currentMode !== 'clickMode') return;
      
      this.isDraggingImage = true;
      this.lastMouseX = event.offsetX;
      this.lastMouseY = event.offsetY;
    },
    handleMouseMove(event) {
      const mouseX = event.offsetX;
      const mouseY = event.offsetY;
      
      if (this.isDraggingImage) {
        const dx = mouseX - this.lastMouseX;
        const dy = mouseY - this.lastMouseY;
      
        this.imageOffsetX += dx;
        this.imageOffsetY += dy;
      
        this.lastMouseX = mouseX;
        this.lastMouseY = mouseY;
      
        this.clearCanvas();
        this.drawImage();
        this.redrawPoints();
        this.redrawPaths();
      } else if (this.isDragging && this.dragPoint && !this.isConfirmingPointEdit) {
        const relativeX = Number(((mouseX - this.imageOffsetX) / this.imageScale).toFixed(1));
        const relativeY = Number(((mouseY - this.imageOffsetY) / this.imageScale).toFixed(1));

        this.tempPoint = {
          x: relativeX,
          y: relativeY,
          tagID: this.dragPoint.tagID,
          tagName: this.dragPoint.tagName
        };
      
        this.clearCanvas();
        this.drawImage();
        this.redrawPoints();
        this.redrawPaths();
        this.drawPoint(relativeX, relativeY, 'green');
      }
    },
    handleMouseUp(event) {
      if (this.isDraggingImage) {
        this.isDraggingImage = false;
      }
      if (this.isDragging && this.dragPoint) {
        const mouseX = Number(((event.offsetX - this.imageOffsetX) / this.imageScale).toFixed(1));
        const mouseY = Number(((event.offsetY - this.imageOffsetY) / this.imageScale).toFixed(1));
      
        this.tempPoint = {
          x: mouseX,
          y: mouseY,
          tagID: this.dragPoint.tagID,
          tagName: this.dragPoint.tagName,
          floor: this.dragPoint.floor,
          floorid: this.dragPoint.floorid
        };
      
        this.isDragging = false;
        this.isConfirmingPointEdit = true;
      
        this.clearCanvas();
        this.drawImage();
        this.redrawPoints();
        this.redrawPaths();
        this.drawPoint(mouseX, mouseY, 'green');
      }
    },
    handleWheel(event) {
      event.preventDefault();
      const zoomIntensity = 0.1;
      const wheel = event.deltaY < 0 ? 1 : -1;
      const zoom = Math.exp(wheel * zoomIntensity);
      
      const mouseX = event.offsetX;
      const mouseY = event.offsetY;
      
      const canvasMouseX = (mouseX - this.imageOffsetX) / this.imageScale;
      const canvasMouseY = (mouseY - this.imageOffsetY) / this.imageScale;
      
      this.imageScale *= zoom;
      
      this.imageOffsetX = mouseX - canvasMouseX * this.imageScale;
      this.imageOffsetY = mouseY - canvasMouseY * this.imageScale;
      
      this.clearCanvas();
      this.drawImage();
      this.redrawPoints();
      this.redrawPaths();
    },
    confirmPointMove() {
      if (this.tempPoint) {
        const index = this.points.findIndex(p => p.tagID === this.dragPoint.tagID);
        if (index !== -1) {
          this.points[index] = { ...this.tempPoint };
        
          this.paths.forEach(path => {
            if (path.start.tagID === this.dragPoint.tagID) {
              path.start.x = this.tempPoint.x;
              path.start.y = this.tempPoint.y;
            }
            if (path.end.tagID === this.dragPoint.tagID) {
              path.end.x = this.tempPoint.x;
              path.end.y = this.tempPoint.y;
            }
          });
        }
      }
      this.isConfirmingPointEdit = false;
      this.isDragging = false;
      this.dragPoint = null;
      this.tempPoint = null;
      this.clearCanvas();
      this.drawImage();
      this.redrawPoints();
      this.redrawPaths();
    },
    cancelPointMove() {
      this.isConfirmingPointEdit = false;
      this.isDragging = false;
      this.dragPoint = null;
      this.tempPoint = null;
      this.clearCanvas();
      this.drawImage();
      this.redrawPoints();
      this.redrawPaths();
    },
    confirmDelete() {
      if (this.deleteType === 'point') {
        this.points = this.points.filter(point => point !== this.deleteTarget);
        this.paths = this.paths.filter(path => 
          !(path.start.x === this.deleteTarget.x && path.start.y === this.deleteTarget.y) &&
          !(path.end.x === this.deleteTarget.x && path.end.y === this.deleteTarget.y)
        );
        this.selectedPoint = null;
      } else if (this.deleteType === 'path') {
        this.paths = this.paths.filter(path => path !== this.deleteTarget);
        this.selectedPath = null;
      }
    
      this.isConfirmingDelete = false;
      this.deleteTarget = null;
      this.deleteType = '';
    
      this.clearCanvas();
      this.drawImage();
      this.redrawPoints();
      this.redrawPaths();
      this.showPopup = false;
    },
    cancelDelete() {
      this.isConfirmingDelete = false;
      this.deleteTarget = null;
      this.deleteType = '';
    },
    handleResize() {
      this.$refs.canvas.width = window.innerWidth * 0.8;
      this.$refs.canvas.height = window.innerHeight * 0.8;
      this.clearCanvas();
      this.drawImage();
      this.redrawPoints();
      this.redrawPaths();
    },
    beforeDestroy() {
      window.removeEventListener('resize', this.handleResize);
    },
    exportCSV() {
      let csvContent = "Tag_ID,Tag_Name,PositionX,PositionY,PositionZ,Floor_ID,Floor_Name,Endpoint1,Endpoint2,speed\n";
      
      this.points.forEach(point => {
        const relatedPaths = this.getRelatedPaths(point);
        const endpoints = relatedPaths.map(path => path.end.tagID);
        
        csvContent += `${point.tagID},${point.tagName},${point.x},${point.y},0,${point.floorid},${point.floor},${endpoints[0] || ''},${endpoints[1] || ''},${relatedPaths[0]?.speed || ''}\n`;
      });

      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      saveAs(blob, "map_data.csv");
    },

    importCSV() {
      this.$refs.fileInput.click();
    },

    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          const content = e.target.result;
          this.parseCSV(content);
        };
        reader.readAsText(file);
      }
    },

    parseCSV(content) {
      const lines = content.split('\n');
      const headers = lines[0].split(',');

      this.points = [];
      this.paths = [];

      for (let i = 1; i < lines.length; i++) {
        const values = lines[i].split(',');
        if (values.length === headers.length) {
          const point = {
            tagID: values[0],
            tagName: values[1],
            x: parseFloat(values[2]),
            y: parseFloat(values[3]),
            floorid: values[5],
            floor: values[6]
          };
          this.points.push(point);

          if (values[7]) {
            this.paths.push({
              start: point,
              end: { tagID: values[7] },
              speed: parseFloat(values[9])
            });
          }
          if (values[8]) {
            this.paths.push({
              start: point,
              end: { tagID: values[8] },
              speed: parseFloat(values[9])
            });
          }
        }
      }
      this.paths.forEach(path => {
        const endPoint = this.points.find(p => p.tagID === path.end.tagID);
        if (endPoint) {
          path.end = { ...endPoint };
        }
      });

      this.clearCanvas();
      this.drawImage();
      this.redrawPoints();
      this.redrawPaths();
    }
  }
};
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  max-width: 100%;
  height: 80vh;
  margin: 0 auto;
  padding: 20px;
}

.main-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.canvas-container {
  background-color: #ffffff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  margin-bottom: 20px;
}

.mode-selection {
  display: flex;
  flex-direction: column;
  background-color: #ffffff;
  padding: 10px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  position: fixed;
  bottom: 40px;
  right: 40px;
}

.mode-selection button {
  margin: 5px 0;
  width: 100%;
  font-size: 18px;
  padding: 15px 20px;
}

.table-btn {
  font-size: 14px;
  padding: 5px 10px;
}

.popup {
  position: fixed;
  top: 20px;
  left: 20px;
  background-color: #ffffff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.2);
  z-index: 1000;
}

.info-table {
  width: 350px;
  background-color: #0E356E;
  padding: 3px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border: none;
  margin-bottom: 10px;
}

.info-table td {
  color: white;
  padding: 5px;
  font-weight: bold;
  text-align: center;
}

.info-table input {
  width: 80%;
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

body {
  font-family: 'Arial', sans-serif;
  background-color: #f0f0f0;
}

button {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px 15px;
  margin: 5px;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s ease;
}

button:hover {
  background-color: #45a049;
  transform: translateY(-2px);
}

button.active {
  background-color: #2196F3;
}

.btn-cancel, .btn-update, .btn-delete {
  color: #ffffff;
  transition: background-color 0.3s ease, transform 0.2s;
}

.btn-update:hover {
  background-color: #FFC107;
  transform: scale(1.05);
}

.btn-delete:hover {
  background-color: #F44336;
  transform: scale(1.05);
}

canvas {
  border: 2px solid #ddd;
  border-radius: 4px;
}

.confirmation-dialog {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: white;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.confirmation-dialog button {
  margin: 0 10px;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin-bottom: 10px;
}

.export-import-buttons {
  position: fixed;
  top: 20px;
  right: 40px;
  display: flex;
  flex-direction: column;
  background-color: #ffffff;
  padding: 10px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.export-import-buttons button {
  margin: 5px 0;
  width: 100%;
  font-size: 18px;
  padding: 15px 20px;
}
</style>