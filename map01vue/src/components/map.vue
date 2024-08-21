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

      <div class="sidebar">
        <div class="export-import-buttons">
          <button @click="exportCSV">匯出</button>
          <button @click="importCSV">匯入</button>
          <input type="file" ref="fileInput" style="display: none;" @change="handleFileUpload">
        </div>
      
        <div class="map-selection">
          <label for="map-select">地圖：</label>
          <select id="map-select" v-model="selectedMap" @change="changeMap">
            <option value="1F">1F</option>
            <option value="4F">4F</option>
          </select>
        </div>
        
        <div class="vehicle-import">
          <label for="vehicle-select">車體：</label>
          <select id="vehicle-select" v-model="selectedVehicle">
            <option value="vehicle1">影像車</option>
            <option value="vehicle2">環境量測</option>
            <option value="vehicle3">車體 3</option>
          </select>
          <button @click="importVehicle">讀取</button>
        </div>

      
        <div class="mode-selection">
          <button :class="{ active: currentMode === 'drawPoint' }" @click="setCurrentMode('drawPoint')">點</button>
          <button :class="{ active: currentMode === 'drawPath' }" @click="setCurrentMode('drawPath')">路徑</button>
          <button :class="{ active: currentMode === 'clickMode' }" @click="setCurrentMode('clickMode')">選點</button>
          <button :class="{ active: currentMode === 'selectPath' }" @click="setCurrentMode('selectPath')">選線</button>
        </div>
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
            <td><input type="text" id="tag-id" v-model="newPoint.tagID" @keydown.stop></td>
          </tr>
          <tr>
            <td><label for="tag-name">Tag_Name</label></td>
            <td><input type="text" id="tag-name" v-model="newPoint.tagName" @keydown.stop></td>
          </tr>
          <tr>
            <td><label for="x-coordinate">X 座標</label></td>
            <td><input type="number" id="x-coordinate" v-model.number="newPoint.x" @keydown.stop></td>
          </tr>
          <tr>
            <td><label for="y-coordinate">Y 座標</label></td>
            <td><input type="number" id="y-coordinate" v-model.number="newPoint.y" @keydown.stop></td>
          </tr>
          <tr>
            <td><label for="floor">樓層</label></td>
            <td><input type="text" id="floor" v-model="newPoint.floor" @keydown.stop></td>
          </tr>
          <tr>
            <td><label for="floorid">樓層編號</label></td>
            <td><input type="text" id="floorid" v-model="newPoint.floorid" @keydown.stop></td>
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
            <td><input type="number" id="path-speed" v-model.number="newPath.speed" min="0" step="0" @keydown.stop></td>
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
              <td><input type="text" v-model="selectedPoint.tagID" :disabled="!isEditingPoint" @keydown.stop></td>
            </tr>
            <tr>
              <td><strong>X 座標</strong></td>
              <td><input type="number" v-model.number="selectedPoint.x" :disabled="!isEditingPoint" @keydown.stop></td>
            </tr>
            <tr>
              <td><strong>Y 座標</strong></td>
              <td><input type="number" v-model.number="selectedPoint.y" :disabled="!isEditingPoint" @keydown.stop></td>
            </tr>
            <tr>
              <td><strong>樓層</strong></td>
              <td><input type="text" v-model="selectedPoint.floor" :disabled="!isEditingPoint" @keydown.stop></td>
            </tr>
            <tr>
              <td><strong>樓層編號</strong></td>
              <td><input type="number" v-model="selectedPoint.floorid" :disabled="!isEditingPoint" @keydown.stop></td>
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
                  <td><input type="number" v-model.number="path.speed" :disabled="!isEditingPath" @keydown.stop></td>
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

      <div v-if="selectedPath">
        <table class="info-table">
          <tr>
            <td colspan="2">路徑資訊</td>
          </tr>
          <tr>
            <td><strong>起點 Tag_ID</strong></td>
            <td>{{ selectedPath.start.tagID }}</td>
          </tr>
          <tr>
            <td><strong>終點 Tag_ID</strong></td>
            <td>{{ selectedPath.end.tagID }}</td>
          </tr>
          <tr>
            <td><strong>起點坐標</strong></td>
            <td>({{ selectedPath.start.x }}, {{ selectedPath.start.y }})</td>
          </tr>
          <tr>
            <td><strong>終點坐標</strong></td>
            <td>({{ selectedPath.end.x }}, {{ selectedPath.end.y }})</td>
          </tr>
          <tr>
            <td><strong>路徑速度</strong></td>
            <td><input type="number" v-model.number="selectedPath.speed" :disabled="!isEditingPath" @keydown.stop></td>
          </tr>
          <tr>
            <td colspan="2">
              <button class="table-btn btn btn-cancel" @click="cancelPathEdit" v-if="isEditingPath">取消修改</button>
              <button class="table-btn btn btn-update" @click="confirmPathEdit" v-if="isEditingPath">確認修改</button>
              <button class="table-btn btn btn-update" @click="enablePathEdit" v-if="!isEditingPath">修改路徑</button>
              <button class="table-btn btn btn-delete" @click="deletePath(selectedPath)">刪除路徑</button>
            </td>
          </tr>
        </table>
      </div>
    </div>

    <div v-if="isConfirmingDelete" class="confirmation-dialog">
      <p>{{ deleteType === 'point' ? '是否要刪除此點？ (相關路徑也會跟著刪除喔！)' : '是否要刪除此路徑？' }}</p>
      <button @click="cancelDelete">取消</button>
      <button @click="confirmDelete">確認</button>
    </div>
    <div v-if="isConfirmingPointEdit" class="confirmation-dialog">
      <p>是否要將點移動到新位置？</p>
      <button @click="cancelPointMove">取消</button>
      <button @click="confirmPointMove">確認</button>
    </div>
    <div v-if="isEditingPointReminder" class="confirmation-dialog">
      <p>您仍在編輯狀態，請先確認修改或取消編輯。</p>
      <button @click="cancelPointEdit">取消</button>
      <button @click="confirmPointEdit">確認修改</button>
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
      currentMode: 'clickMode',
      points: [],
      selectedPoint: null,
      addingPoint: false,
      defaultTagID: '',
      floor:'1F',
      floorid: 2,
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
      isEditingPointReminder: false,
      pathStartPoint: null,
      tempPath: null,
      selectedMap: '1F',
      selectedVehicle: 'vehicle1',
      mapImages: {
        '1F': require('@/assets/MAP1F1.png'),
        '4F': require('@/assets/MAP4F1.png')
      },
      hoveredPath: null,
      hoveredPoint: null,
    };
  },
  mounted() {
    this.context = this.$refs.canvas.getContext('2d');
    this.loadImage();
    this.defaultTagID = this.getNextTagID();

    this.$refs.canvas.width = window.innerWidth * 0.8;
    this.$refs.canvas.height = window.innerHeight * 0.8;

    window.addEventListener('resize', this.handleResize);
    window.addEventListener('keydown', this.handleKeyPress);

  },
  methods: {
    changeMap() {
      this.image.src = this.mapImages[this.selectedMap];
      if(this.selectedMap === '1F'){
        this.floor = '1F';
        this.floorid = 2;
      } else if(this.selectedMap === '4F'){
        this.floor = '4F';
        this.floorid = 5;
      }
      this.image.onload = () => {
        this.clearCanvas();
        this.drawImage();
        this.points = [];
        this.paths = [];
      };
    },
    importVehicle() {
      console.log(`導入車體: ${this.selectedVehicle}`);
    },
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
      if (this.isEditingPoint) {
        this.isEditingPointReminder = true;
        return;
      }
      this.cleanupCurrentMode();
      this.currentMode = mode;
      if (mode !== 'drawPath') {
        this.clearPathPreview();
      }
      this.showPopup = false;
    },
    cleanupCurrentMode() {
      this.selectedPoint = null;
      this.selectedPath = null;
      this.addingPoint = false;
      this.isEditingPoint = false;
      this.isEditingPath = false;
      this.pathPoints = [];
      this.tempPath = null;
      this.isConfirmingPointEdit = false;
      this.isConfirmingDelete = false;
      this.showPopup = false;
      this.isEditingPointReminder = false;

      this.clearCanvas();
      this.redrawPoints();
      this.redrawPaths();
    },
    handleCanvasClick(event) {
  const mouseX = Math.round((event.offsetX - this.imageOffsetX) / this.imageScale);
  const mouseY = Math.round((event.offsetY - this.imageOffsetY) / this.imageScale);

  if (!this.isEditingPoint) {
    this.cleanupPreviousState();
  }
  
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
    this.selectNearestPoint(mouseX, mouseY);
  } else if (this.currentMode === 'drawPath') {
    this.addPathPoint(mouseX, mouseY);
  } else if (this.currentMode === 'selectPath') {
    this.selectNearestPath(mouseX, mouseY);
  }
},
selectNearestPoint(mouseX, mouseY) {
  let nearestPoint = null;
  let minDistance = Infinity;
  const baseClickThreshold = 10;
  const clickThreshold = Math.min(baseClickThreshold / this.imageScale, 5);

  for (const point of this.points) {
    const distance = Math.sqrt(Math.pow(point.x - mouseX, 2) + Math.pow(point.y - mouseY, 2));
    if (distance < minDistance && distance <= clickThreshold) {
      minDistance = distance;
      nearestPoint = point;
    }
  }

  if (nearestPoint) {
    this.selectedPoint = nearestPoint;
    this.selectedPath = null;
    this.showPopup = true;
    this.clearCanvas();
    this.redrawPoints();
    this.redrawPaths();
    this.drawPoint(nearestPoint.x, nearestPoint.y, 'green');
  } else {
    this.selectedPoint = null;
    this.selectedPath = null;
    this.showPopup = false;
  }
},
  selectNearestPath(mouseX, mouseY) {
    let nearestPath = null;
    let minDistance = Infinity;
    const baseClickThreshold = 8;
    const clickThreshold = Math.min(baseClickThreshold / this.imageScale, 3);

    for (const path of this.paths) {
      const distance = this.distanceToPath(mouseX, mouseY, path);
      if (distance < minDistance && distance <= clickThreshold) {
        minDistance = distance;
        nearestPath = path;
      }
    }

    if (nearestPath) {
      this.selectedPath = nearestPath;
      this.selectedPoint = null;
      this.showPopup = true;
      this.clearCanvas();
      this.redrawPoints();
      this.redrawPaths();
      this.highlightPath(nearestPath);
    } else {
      this.selectedPath = null;
      this.selectedPoint = null;
      this.showPopup = false;
    }
  },
  highlightPath(path, color = 'red', lineWidth = 3) {
    const startX = this.imageOffsetX + path.start.x * this.imageScale;
    const startY = this.imageOffsetY + path.start.y * this.imageScale;
    const endX = this.imageOffsetX + path.end.x * this.imageScale;
    const endY = this.imageOffsetY + path.end.y * this.imageScale;

    this.context.beginPath();
    this.context.moveTo(startX, startY);
    this.context.lineTo(endX, endY);
    this.context.strokeStyle = color;
    this.context.lineWidth = lineWidth;
    this.context.stroke();
  },
  distanceToPath(x, y, path) {
    const x1 = path.start.x;
    const y1 = path.start.y;
    const x2 = path.end.x;
    const y2 = path.end.y;

    const A = x - x1;
    const B = y - y1;
    const C = x2 - x1;
    const D = y2 - y1;

    const dot = A * C + B * D;
    const len_sq = C * C + D * D;
    let param = -1;
    if (len_sq != 0) param = dot / len_sq;

    let xx, yy;

    if (param < 0) {
      xx = x1;
      yy = y1;
    } else if (param > 1) {
      xx = x2;
      yy = y2;
    } else {
      xx = x1 + param * C;
      yy = y1 + param * D;
    }

    const dx = x - xx;
    const dy = y - yy;
    return Math.sqrt(dx * dx + dy * dy);
  },
    cleanupPreviousState() {
      this.showPopup = false;
      this.isEditingPoint = false;
      this.isEditingPath = false;
      this.isConfirmingPointEdit = false;
      this.isConfirmingDelete = false;
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
        x: Math.round(this.newPoint.x),
        y: Math.round(this.newPoint.y),
        tagID: this.newPoint.tagID,
        tagName: this.newPoint.tagName,
        floor: this.newPoint.floor,
        floorid: this.newPoint.floorid
      });
    
      this.drawPoint(Math.round(this.newPoint.x), Math.round(this.newPoint.y));
      this.resetNewPoint();
    },
    cancelAddPoint() {
      this.resetNewPoint();
      this.clearCanvas();
      this.redrawPoints();
      this.redrawPaths();
      this.showPopup = false;
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
      this.defaultTagID = (parseInt(this.defaultTagID) + 1).toString().padStart(4, '0');
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

      if (this.hoveredPoint && this.hoveredPoint.x === x && this.hoveredPoint.y === y) {
        this.context.beginPath();
        this.context.arc(canvasX, canvasY, 10, 0, Math.PI * 2);
        this.context.strokeStyle = 'yellow';
        this.context.lineWidth = 3;
        this.context.stroke();
      }

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
      const clickThreshold = 10 / this.imageScale;

      for (const point of this.points) {
        if (Math.abs(point.x - mouseX) <= clickThreshold && Math.abs(point.y - mouseY) <= clickThreshold) {
          clickedPoint = point;
          break;
        }
      }

      if (clickedPoint) {
        if (this.pathPoints.length === 0) {
          this.pathStartPoint = clickedPoint;
          this.drawPoint(clickedPoint.x, clickedPoint.y, 'red');
          this.pathPoints.push(clickedPoint);
        } else if (this.pathPoints.length === 1) {
          if (clickedPoint.tagID !== this.pathStartPoint.tagID) {
            this.pathPoints.push(clickedPoint);
            this.tempPath = {
              start: this.pathStartPoint,
              end: clickedPoint
            };
            this.drawDashedLine(this.pathStartPoint.x, this.pathStartPoint.y, clickedPoint.x, clickedPoint.y);
            this.showPopup = true;
          } else {
            this.clearPathPreview();
            alert("起點與終點不能是同一個點，請重新繪製。");
          }
        }

        this.showFeedback(clickedPoint.x, clickedPoint.y, 'green');
      } else {
        this.showFeedback(mouseX, mouseY, 'red');
      }
    },
    showFeedback(x, y, color) {
      const canvasX = this.imageOffsetX + x * this.imageScale;
      const canvasY = this.imageOffsetY + y * this.imageScale;

      this.context.beginPath();
      this.context.arc(canvasX, canvasY, 8, 0, Math.PI * 2);
      this.context.fillStyle = color;
      this.context.globalAlpha = 0.5;
      this.context.fill();
      this.context.globalAlpha = 1;

      setTimeout(() => {
        this.clearCanvas();
        this.redrawPoints();
        this.redrawPaths();
        if (this.pathStartPoint) {
          this.drawPoint(this.pathStartPoint.x, this.pathStartPoint.y, 'red');
        }
      }, 300);
    },
    clearPathPreview() {
      this.pathStartPoint = null;
      this.pathPoints = [];
      this.tempPath = null;
      this.clearCanvas();
      this.redrawPoints();
      this.redrawPaths();
    },
    confirmAddPath() {
      if (this.tempPath) {
        const path = {
          start: this.tempPath.start,
          end: this.tempPath.end,
          speed: this.newPath.speed
        };
      
        this.paths.push(path);
      
        this.clearPathPreview();
        this.clearCanvas();
        this.redrawPoints();
        this.redrawPaths();
        this.showPopup = false;
      }
    },
    cancelAddPath() {
      this.clearPathPreview();
      this.showPopup = false;
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
        path.start.tagID === point.tagID || path.end.tagID === point.tagID
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
        if (point && point.x !== undefined && point.y !== undefined) {
          this.drawPoint(point.x, point.y);
        }
      }
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
    redrawPaths() {
    this.context.beginPath();
    this.context.strokeStyle = 'black';
    this.context.lineWidth = 1;
      
    for (const path of this.paths) {
      if (path.start && path.end && 
          this.points.some(p => p.tagID === path.start.tagID) && 
          this.points.some(p => p.tagID === path.end.tagID)) {
        this.drawLine(path.start.x, path.start.y, path.end.x, path.end.y);
      }
    }
  
    if (this.tempPath) {
      this.drawDashedLine(this.tempPath.start.x, this.tempPath.start.y, this.tempPath.end.x, this.tempPath.end.y);
    }

    if (this.hoveredPath) {
      this.highlightPath(this.hoveredPath, 'red', 2);
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
      if (!this.selectedPoint.tagID || !this.selectedPoint.tagName || 
          this.selectedPoint.x === undefined || this.selectedPoint.y === undefined || 
          !this.selectedPoint.floor || !this.selectedPoint.floorid) {
        alert('請填寫所有必填欄位！');
        return;
      }
    
      const index = this.points.findIndex(p => p.tagID === this.originalPoint.tagID);
      if (index !== -1) {
        this.points[index] = { ...this.selectedPoint };
      
        this.paths.forEach(path => {
          if (path.start.tagID === this.originalPoint.tagID) {
            path.start = { ...this.selectedPoint };
          }
          if (path.end.tagID === this.originalPoint.tagID) {
            path.end = { ...this.selectedPoint };
          }
        });
      }
      this.isEditingPoint = false;
      this.dragPoint = null;
      this.originalPoint = {};
    
      this.clearCanvas();
      this.redrawPoints();
      this.redrawPaths();
      this.isEditingPointReminder = false;
      this.showPopup = true;
    },
    cancelPointEdit() {
      if (this.originalPoint) {
        const index = this.points.findIndex(p => p.tagID === this.originalPoint.tagID);
        if (index !== -1) {
          this.points[index] = { ...this.originalPoint };
          this.selectedPoint = { ...this.originalPoint };
        }
      }
      this.isEditingPoint = false;
      this.isConfirmingPointEdit = false;
      this.originalPoint = {};
      this.originalPath = {};
    
      this.clearCanvas();
      this.redrawPoints();
      this.redrawPaths();
      this.isEditingPointReminder = false;
      this.showPopup = false;
    },
    closePopup() {
      this.showPopup = false;
      this.cleanupCurrentMode();
    },
    checkEditingStatus() {
      if (this.isEditingPoint) {
        this.isEditingPointReminder = true;
        return true;
      }
      return false;
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
  if (this.currentMode !== 'clickMode' && this.currentMode !== 'selectPath') return;
  
  this.isDraggingImage = true;
  this.lastMouseX = event.offsetX;
  this.lastMouseY = event.offsetY;
},
    handleMouseMove(event) {
  const mouseX = event.offsetX;
  const mouseY = event.offsetY;
  
  if (this.isDraggingImage && !this.selectedPath) {
    const dx = mouseX - this.lastMouseX;
    const dy = mouseY - this.lastMouseY;
  
    this.imageOffsetX += dx;
    this.imageOffsetY += dy;
  
    this.lastMouseX = mouseX;
    this.lastMouseY = mouseY;
  
    this.redrawAll();
  } else if (this.isDragging && this.dragPoint && !this.isConfirmingPointEdit) {
    const relativeX = Math.round((mouseX - this.imageOffsetX) / this.imageScale);
    const relativeY = Math.round((mouseY - this.imageOffsetY) / this.imageScale);

    this.tempPoint = {
      ...this.dragPoint,
      x: relativeX,
      y: relativeY
    };

    if (this.selectedPoint) {
      this.selectedPoint.x = relativeX;
      this.selectedPoint.y = relativeY;
    }
    this.redrawAll();
    this.drawPoint(relativeX, relativeY, 'green');
  }

  const relativeX = Math.round((mouseX - this.imageOffsetX) / this.imageScale);
  const relativeY = Math.round((mouseY - this.imageOffsetY) / this.imageScale);

  if (this.currentMode === 'selectPath') {
    let nearestPath = null;
    let minDistance = Infinity;
    const hoverThreshold = 10 / this.imageScale;

    for (const path of this.paths) {
      const distance = this.distanceToPath(relativeX, relativeY, path);
      if (distance < minDistance && distance <= hoverThreshold) {
        minDistance = distance;
        nearestPath = path;
      }
    }

    if (nearestPath !== this.hoveredPath) {
      this.hoveredPath = nearestPath;
      this.redrawAll();
      if (this.hoveredPath) {
        this.highlightPath(this.hoveredPath, 'red', 2);
      }
    }
  } else if (this.currentMode === 'clickMode') {
    let hoveredPoint = null;
    const hoverThreshold = 10 / this.imageScale;

    for (const point of this.points) {
      const distance = Math.sqrt(Math.pow(point.x - relativeX, 2) + Math.pow(point.y - relativeY, 2));
      if (distance <= hoverThreshold) {
        hoveredPoint = point;
        break;
      }
    }

    if (hoveredPoint !== this.hoveredPoint) {
      this.hoveredPoint = hoveredPoint;
      this.redrawAll();
    }
  }
},
handleMouseUp(event) {
  if (this.isDraggingImage) {
    this.isDraggingImage = false;
  }
  if (this.isDragging && this.dragPoint) {
    const mouseX = Math.round((event.offsetX - this.imageOffsetX) / this.imageScale);
    const mouseY = Math.round((event.offsetY - this.imageOffsetY) / this.imageScale);
  
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
  
    this.redrawAll();
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
          this.selectedPoint = { ...this.tempPoint };
        
          this.paths.forEach(path => {
            if (path.start.tagID === this.dragPoint.tagID) {
              path.start = { ...this.tempPoint };
            }
            if (path.end.tagID === this.dragPoint.tagID) {
              path.end = { ...this.tempPoint };
            }
          });
        }
      }
      this.isConfirmingPointEdit = false;
      this.isEditingPoint = false;
      this.isDragging = false;
      this.dragPoint = null;
      this.tempPoint = null;
      this.clearCanvas();
      this.drawImage();
      this.redrawPoints();
      this.redrawPaths();
      this.showPopup = true;
    },
    cancelPointMove() {
      this.isConfirmingPointEdit = false;
      this.isEditingPoint = false;
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
        const deletedPointTagID = this.deleteTarget.tagID;
        this.points = this.points.filter(point => point.tagID !== deletedPointTagID);
        this.paths = this.paths.filter(path => 
          path.start.tagID !== deletedPointTagID && path.end.tagID !== deletedPointTagID
        );
        this.selectedPoint = null;
      } else if (this.deleteType === 'path') {
        this.paths = this.paths.filter(path => path !== this.deleteTarget);
        this.selectedPath = null;
      }
    
      this.isConfirmingDelete = false;
      this.isEditingPoint = false;
      this.isConfirmingPointEdit = false;
      this.deleteTarget = null;
      this.deleteType = '';
    
      this.redrawAll();
      this.showPopup = false;
    },
    redrawAll() {
      this.clearCanvas();
      this.drawImage();
      this.redrawPoints();
      this.redrawPaths();
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
      window.removeEventListener('keydown', this.handleKeyPress);
    },
    exportCSV() {
      let csvContent = "Tag_ID,Tag_Name,PositionX,PositionY,PositionZ,Floor_ID,Floor_Name,Endpoint1,Endpoint2,Speed1,Speed2\n";
        
      this.points.forEach(point => {
        const relatedPaths = this.getRelatedPaths(point);
        const endpoints = relatedPaths.map(path => path.end.tagID);
        const speeds = relatedPaths.map(path => path.speed);
      
        csvContent += `${point.tagID},${point.tagName},${point.x},${point.y},0,${point.floorid},${point.floor},${endpoints[0] || ''},${endpoints[1] || ''},${speeds[0] || ''},${speeds[1] || ''}\n`;
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

      let maxTagID = 0;

      for (let i = 1; i < lines.length; i++) {
        const values = lines[i].split(',');
        if (values.length === headers.length) {
          const tagID = parseInt(values[0]);
          if (tagID > maxTagID) {
            maxTagID = tagID;
          }
        
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
              speed: parseFloat(values[10])
            });
          }
        }
      }
      this.defaultTagID = (maxTagID + 1).toString().padStart(4, '0');
    
      this.paths.forEach(path => {
        const endPoint = this.points.find(p => p.tagID === path.end.tagID);
        if (endPoint) {
          path.end = { ...endPoint };
        }
      });
      this.redrawAll();
    },
    handleKeyPress(event) {
      if (event.key === 'Enter') {
        if (this.addingPoint) {
          this.confirmAddPoint();
        } else if (this.currentMode === 'drawPath' && this.pathPoints.length === 2) {
          this.confirmAddPath();
        } else if (this.isEditingPoint && !this.isConfirmingPointEdit) {
          this.confirmPointEdit();
        } else if (this.isConfirmingPointEdit) {
          this.confirmPointMove();
        } else if (this.isEditingPath) {
          this.confirmPathEdit();
        } else if (this.isConfirmingDelete) {
          this.confirmDelete();
        }
      } else if (event.key === 'Escape') {
        if (this.addingPoint) {
          this.cancelAddPoint();
        } else if (this.currentMode === 'drawPath' && this.pathPoints.length === 2) {
          this.cancelAddPath();
        } else if (this.isEditingPoint && !this.isConfirmingPointEdit) {
          this.cancelPointEdit();
        } else if (this.isConfirmingPointEdit) {
          this.cancelPointMove();
        } else if (this.isEditingPath) {
          this.cancelPathEdit();
        } else if (this.isConfirmingDelete) {
          this.cancelDelete();
        }
      }
    },
  }
};
</script>

<style scoped>
.container {
  display: flex;
  justify-content: space-between;
  max-width: 100%;
  height: 80vh;
  margin: 0 auto;
  padding: 20px;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.sidebar {
  width: 100px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  position: fixed;
  top: 260px;
  right: 40px;
}

.export-import-buttons,
.map-selection,
.vehicle-import,
.mode-selection {
  background-color: #ffffff;
  padding: 10px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.export-import-buttons button,
.vehicle-import button,
.mode-selection button {
  width: 100%;
  margin: 5px 0;
  font-size: 16px;
  padding: 10px;
}

select {
  display: block;
  width: 100%;
  margin: 5px 0;
  padding: 5px;
  font-size: 16px;
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

.info-table input:disabled {
  background-color: #f0f0f0;
  color: #666;
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