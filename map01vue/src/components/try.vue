<template>
  <div>
    <!-- Mode selection -->
    <div>
      <label>選擇繪圖模式：</label>
      <button :class="{ active: currentMode === 'drawPoint' }" @click="setCurrentMode('drawPoint')">點</button>
      <button :class="{ active: currentMode === 'drawPath' }" @click="setCurrentMode('drawPath')">點路徑</button>
      <button :class="{ active: currentMode === 'clickMode' }" @click="setCurrentMode('clickMode')">點選</button>
      <button :class="{ active: currentMode === 'continuousdraw' }" @click="setCurrentMode('continuousdraw')">連續繪圖</button>
    </div>

    <!-- Canvas -->
    <canvas ref="canvas" width="600" height="400"
            @click="handleCanvasClick"
            style="border:1px solid #000;">
      Your browser does not support the HTML5 canvas tag.
    </canvas>

    <!-- Input point info -->
    <div v-if="currentMode === 'drawPoint' && addingPoint">
      <table class="info-table">
        <tr>
          <td colspan="2">新增點</td>
        </tr>
        <tr>
          <td><label for="tag-id">Tag_ID</label></td>
          <td><input type="text" id="tag-id" v-model="newPoint.tagID" :placeholder="getNextTagID()"></td>
        </tr>
        <tr>
          <td><label for="tag-name">Tag_Name</label></td>
          <td><input type="text" id="tag-name" v-model="newPoint.tagName" :placeholder="getNextTagID()"></td>
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
          <td colspan="2">
            <button class="btn btn-delete" @click="cancelAddPoint">取消</button>
            <button @click="confirmAddPoint">確認新增</button>
          </td>
        </tr>
      </table>
    </div>

    <!-- Input path info -->
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
            <button class="btn btn-delete" @click="cancelAddPath">取消</button>
            <button @click="confirmAddPath">確認新增</button>
          </td>
        </tr>
      </table>
    </div>

    <!-- Display point and path info -->
    <div v-if="selectedPoint || selectedPath" style="margin-top: 10px;">
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
            <td colspan="2">
              <button class="btn btn-cancel" @click="cancelPointEdit(selectedPoint)" v-if="isEditingPoint">取消修改</button>
              <button class="btn btn-update" @click="confirmPointEdit" v-if="isEditingPoint">確認修改</button>
              <button class="btn btn-update" @click="enablePointEdit(selectedPoint)" v-if="!isEditingPoint">修改點</button>
              <button class="btn btn-delete" @click="deletePoint(selectedPoint)">刪除點</button>
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
                  <button class="btn btn-cancel" @click="cancelPathEdit" v-if="isEditingPath">取消修改</button>
                  <button class="btn btn-update" @click="confirmPathEdit" v-if="isEditingPath">確認修改</button>
                  <button class="btn btn-update" @click="enablePathEdit(path)" v-if="!isEditingPath">修改路徑</button>
                  <button class="btn btn-delete" @click="deletePath(path)">刪除路徑</button>
                </td>
              </tr>
            </table>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
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
        tagName: ''
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
    };
  },
  mounted() {
    this.context = this.$refs.canvas.getContext('2d');
    this.loadImage();
    this.defaultTagID = this.getNextTagID();
    this.$refs.canvas.addEventListener('mousemove', this.handleMouseMove);
    this.$refs.canvas.addEventListener('mouseup', this.handleMouseUp);
    this.$refs.canvas.addEventListener('mousedown', this.handleImageMouseDown);
    this.$refs.canvas.addEventListener('wheel', this.handleWheel, { passive: false });
  },
  methods: {
    loadImage() {
  this.image = new Image();
  this.image.src = 'https://via.placeholder.com/1000';
  this.image.onload = () => {
    this.imageX = (this.$refs.canvas.width - this.image.width) / 2;
    this.imageY = (this.$refs.canvas.height - this.image.height) / 2;
    this.drawImage();
  };
},

drawImage() {
  if (this.image) {
    this.context.drawImage(this.image, this.imageX, this.imageY);
  }
},

    
    setCurrentMode(mode) {
      this.currentMode = mode;
      if (mode !== 'drawPath') {
        this.clearPathPreview();
      }
    },
    handleCanvasClick(event) {
      const mouseX = (event.offsetX - this.imageX) / this.scale;
      const mouseY = (event.offsetY - this.imageY) / this.scale;

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
        return (maxID + 1).toString();
      }
    },
    confirmAddPoint() {
      if (this.newPoint.tagID === '' || this.newPoint.tagName === '' || this.newPoint.x === 0 || this.newPoint.y === 0) {
        alert('請填寫所有必填欄位！');
        return;
      }
    
      this.points.push({
        x: this.newPoint.x,
        y: this.newPoint.y,
        tagID: this.newPoint.tagID,
        tagName: this.newPoint.tagName
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
      this.newPoint.x = 0;
      this.newPoint.y = 0;
      this.newPoint.tagID = '';
      this.newPoint.tagName = '';
      this.addingPoint = false;
    },
    drawPoint(x, y, color = 'blue') {
  const canvasX = this.imageX + x * this.scale;
  const canvasY = this.imageY + y * this.scale;
  this.context.beginPath();
  this.context.arc(canvasX, canvasY, 3 * this.scale, 0, Math.PI * 2);
  this.context.fillStyle = color;
  this.context.fill();

  const tagID = this.points.find(point => point.x === x && point.y === y)?.tagID;
  if (tagID) {
    this.context.font = `${12 * this.scale}px Arial`;
    this.context.fillStyle = 'black';
    this.context.fillText(`${tagID}`, canvasX + 5 * this.scale, canvasY - 5 * this.scale);
  }
},

    addPathPoint(mouseX, mouseY) {
      let clickedPoint = null;
      for (const point of this.points) {
        if (Math.abs(point.x - mouseX) <= 3 && Math.abs(point.y - mouseY) <= 3) {
          clickedPoint = point;
          break;
        }
      }
      if (clickedPoint) {
        this.pathPoints.push({ x: clickedPoint.x, y: clickedPoint.y, tagID: clickedPoint.tagID });

        if (this.pathPoints.length === 2) {
          const startPoint = this.pathPoints[0];
          const endPoint = this.pathPoints[1];
          
          this.newPath.endX = endPoint.x;
          this.newPath.endY = endPoint.y;

          this.drawDashedLine(startPoint.x, startPoint.y, endPoint.x, endPoint.y);
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
    },
    cancelAddPath() {
      this.clearPathPreview();
      this.pathPoints = [];
    },
    clearPathPreview() {
      this.clearCanvas();
      this.redrawPoints();
      this.redrawPaths();
    },
    drawDashedLine(x1, y1, x2, y2) {
      this.context.beginPath();
      this.context.setLineDash([5, 5]);
      this.context.moveTo(x1, y1);
      this.context.lineTo(x2, y2);
      this.context.strokeStyle = 'gray';
      this.context.stroke();
      this.context.setLineDash([]);
    },
    showPointInfo(mouseX, mouseY) {
      for (const point of this.points) {
        if (Math.abs(point.x - mouseX) <= 3 && Math.abs(point.y - mouseY) <= 3) {
          this.selectedPoint = point;
          this.selectedPath = null; 

          this.clearCanvas();
          this.redrawPoints();
          this.redrawPaths();
          this.drawPoint(point.x, point.y, 'green');
          return;
        }
      }
      this.selectedPoint = null;
      this.selectedPath = null;
    },
    getRelatedPaths(point) {
      return this.paths.filter(path => 
        path.start.x === point.x && path.start.y === point.y
      );
    },
    deletePoint(pointToDelete) {
      if (confirm("請問要刪除此點嗎？ (相關路徑也會跟著刪除喔！)")) {
        this.points = this.points.filter(point => point !== pointToDelete);

        this.paths = this.paths.filter(path => 
          !(path.start.x === pointToDelete.x && path.start.y === pointToDelete.y) &&
          !(path.end.x === pointToDelete.x && path.end.y === pointToDelete.y)
        );
        this.selectedPoint = null;
        this.selectedPath = null;

        this.clearCanvas();
        this.redrawPoints();
        this.redrawPaths();
      }
    },
    deletePath(pathToDelete) {
      if (confirm("請問要刪除此路徑嗎?")) {
        this.paths = this.paths.filter(path => path !== pathToDelete);
        this.selectedPath = null;

        this.clearCanvas();
        this.redrawPoints();
        this.redrawPaths();
      }
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
  const canvasX1 = this.imageX + x1 * this.scale;
  const canvasY1 = this.imageY + y1 * this.scale;
  const canvasX2 = this.imageX + x2 * this.scale;
  const canvasY2 = this.imageY + y2 * this.scale;
  
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
          path.start.x = this.selectedPoint.x;
          path.start.y = this.selectedPoint.y;
        }
        if (path.end.x === this.originalPoint.x && path.end.y === this.originalPoint.y) {
          path.end.x = this.selectedPoint.x;
          path.end.y = this.selectedPoint.y;
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
  const mouseX = event.offsetX;
  const mouseY = event.offsetY;

  if (
    mouseX >= this.imageX &&
    mouseX <= this.imageX + this.image.width * this.scale &&
    mouseY >= this.imageY &&
    mouseY <= this.imageY + this.image.height * this.scale
  ) {
    this.isDraggingImage = true;
    this.dragOffsetX = mouseX - this.imageX;
    this.dragOffsetY = mouseY - this.imageY;
  }
},

    handleMouseMove(event) {
      const mouseX = event.offsetX;
      const mouseY = event.offsetY;

      if (this.isDraggingImage) {
    this.imageX = mouseX - this.dragOffsetX;
    this.imageY = mouseY - this.dragOffsetY;

    this.clearCanvas();
    this.drawImage();
    this.redrawPoints();
    this.redrawPaths();
  }
      if (this.isDragging && this.dragPoint) {
        this.clearCanvas();
        this.redrawPoints();
        this.redrawPaths();
        this.drawPoint(mouseX, mouseY, 'green');
      }
    },
    handleMouseUp(event) {
      if (this.isDraggingImage) {
        this.isDraggingImage = false;
      }
      if (this.isDragging) {
        const mouseX = event.offsetX;
        const mouseY = event.offsetY;

        if (this.dragPoint && confirm(`Do you want to place the point at (${mouseX}, ${mouseY})?`)) {
          const dx = mouseX - this.dragPoint.x;
          const dy = mouseY - this.dragPoint.y;

          this.dragPoint.x += dx;
          this.dragPoint.y += dy;

          this.paths.forEach(path => {
            if (path.start === this.dragPoint) {
              path.start.x += dx;
              path.start.y += dy;
            }
            if (path.end === this.dragPoint) {
              path.end.x += dx;
              path.end.y += dy;
            }
          });
          this.clearCanvas();
          this.redrawPoints();
          this.redrawPaths();
        }
        if (this.dragPoint) {
          this.drawPoint(this.dragPoint.x, this.dragPoint.y, 'green');
        }
        this.isDragging = false;
        this.dragPoint = null;
      }
    },
    beforeDestroy() {
      this.$refs.canvas.removeEventListener('mousemove', this.handleMouseMove);
      this.$refs.canvas.removeEventListener('mouseup', this.handleMouseUp);
      this.$refs.canvas.removeEventListener('mousedown', this.handleImageMouseDown);
      this.$refs.canvas.removeEventListener('wheel', this.handleWheel);
    },
    handleWheel(event) {
  event.preventDefault();
  const zoomIntensity = 0.1;
  const wheel = event.deltaY < 0 ? 1 : -1;
  const zoom = Math.exp(wheel * zoomIntensity);
  
  const mouseX = event.offsetX;
  const mouseY = event.offsetY;

  const canvasMouseX = (mouseX - this.imageX) / this.scale;
  const canvasMouseY = (mouseY - this.imageY) / this.scale;

  this.scale *= zoom;

  this.imageX = mouseX - canvasMouseX * this.scale;
  this.imageY = mouseY - canvasMouseY * this.scale;

  this.clearCanvas();
  this.drawImage();
  this.redrawPoints();
  this.redrawPaths();
},
  }
};
</script>

<style scoped>
.info-table {
  width: 350px;
  background-color: #0E356E;
  padding: 3px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border: none;
}

.info-table td {
  color: white;
  padding: 5px;
  font-weight: bold;
  text-align: center;
}

.info-table input {
  width: 80%;
}

button {
  padding: 5px 10px;
  margin: 0 5px;
  cursor: pointer;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  color: #fff;
  transition: background-color 0.3s ease, transform 0.2s;
}

button.active {
  background-color: #4CAF50;
}

button:hover {
  background-color: #45a049;
  transform: scale(1.05);
}

.btn-cancel, .btn-update, .btn-delete {
  color: #ffffff;
  transition: background-color 0.3s ease, transform 0.2s;
}

.btn-update:hover {
  background-color: #FFC107;
  transform: scale(1.05);

}.btn-delete:hover {
  background-color: #F44336;
  transform: scale(1.05);
}

canvas {
  border: 1px solid #000;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin-bottom: 10px;
}
</style>
