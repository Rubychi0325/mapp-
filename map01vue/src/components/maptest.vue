<template>
  <div>
    <div>
      <label>選擇繪圖模式：</label>
      <button :class="{ active: currentMode === 'drawPoint' }" @click="setCurrentMode('drawPoint')">點</button>
      <button :class="{ active: currentMode === 'drawPath' }" @click="setCurrentMode('drawPath')">點路徑</button>
      <button :class="{ active: currentMode === 'clickMode' }" @click="setCurrentMode('clickMode')">點選</button>
      <button :class="{ active: currentMode === 'Dragdrop' }" @click="setCurrentMode('Dragdrop')">拖曳點</button>
      <button :class="{ active: currentMode === 'continuousdraw' }" @click="setCurrentMode('continuousdraw')">連續繪圖</button>
    </div>

    <canvas ref="canvas" width="600" height="400"
            @click="handleCanvasClick"
            style="border:1px solid #000;">
      Your browser does not support the HTML5 canvas tag.
    </canvas>

    <div v-if="isDragging && draggedPoint" style="position: absolute; background: rgba(255, 255, 255, 0.7); padding: 5px; border-radius: 5px;">
      <strong>坐標:</strong> ({{ draggedPoint.x.toFixed(2) }}, {{ draggedPoint.y.toFixed(2) }})
    </div>

    <div v-if="currentMode === 'drawPoint' && addingPoint">
      <table>
        <tr style="background-color: #0E356E;">
          <td colspan="2" style="color: white; text-align: center; padding: 10px; border-radius: 8px; font-weight: bold; font-size: 18px;">新增點</td>
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
          <td><button @click="cancelAddPoint">取消</button></td>
          <td><button @click="confirmAddPoint">確認新增</button></td>
        </tr>
      </table>
    </div>

    <div v-if="selectedPoint" style="margin-top: 10px;">
      <table>
        <tr style="background-color: #0E356E;">
          <td colspan="2" style="color: white; text-align: center; padding: 10px; border-radius: 8px; font-weight: bold; font-size: 18px;">點資訊</td>
        </tr>
        <tr>
          <td><strong>Tag_ID</strong></td>
          <td>
            <input type="text" v-model="selectedPoint.tagID" :disabled="!isEditingPoint">
          </td>
        </tr>
        <tr>
          <td><strong>X 座標</strong></td>
          <td>
            <input type="number" v-model.number="selectedPoint.x" :disabled="!isEditingPoint">
          </td>
        </tr>
        <tr>
          <td><strong>Y 座標</strong></td>
          <td>
            <input type="number" v-model.number="selectedPoint.y" :disabled="!isEditingPoint">
          </td>
        </tr>
        <tr>
          <td colspan="2">
            <button @click="cancelPointEdit(selectedPoint)" v-if="isEditingPoint">取消修改</button>
            <button @click="confirmPointEdit" v-if="isEditingPoint">確認修改</button>
            <button @click="enablePointEdit(selectedPoint)" v-if="!isEditingPoint">修改點</button>
            <button @click="deletePoint(selectedPoint)">刪除點</button>
          </td>
        </tr>
      </table>
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
      newPoint: {
        x: 0,
        y: 0,
        tagID: '',
        tagName: ''
      },
      isDragging: false,
      draggedPoint: null,
      offsetX: 0,
      offsetY: 0,
      originalPosition: null, // 儲存原始位置
    };
  },
  mounted() {
    this.context = this.$refs.canvas.getContext('2d');
    this.$refs.canvas.addEventListener('mousemove', this.handleMouseMove);
    this.$refs.canvas.addEventListener('mouseup', this.handleMouseUp);
  },
  methods: {
    setCurrentMode(mode) {
      this.currentMode = mode;
      this.addingPoint = mode === 'drawPoint';
    },
    handleCanvasClick(event) {
      const mouseX = event.offsetX;
      const mouseY = event.offsetY;

      if (this.currentMode === 'drawPoint') {
        this.newPoint.x = mouseX;
        this.newPoint.y = mouseY;
        this.addingPoint = true;
      } else if (this.currentMode === 'clickMode') {
        this.showPointInfo(mouseX, mouseY);
      } else if (this.currentMode === 'Dragdrop') {
        this.points.forEach(point => {
          if (Math.abs(point.x - mouseX) <= 3 && Math.abs(point.y - mouseY) <= 3 && !this.isDragging) {
            this.isDragging = true;
            this.draggedPoint = point;
            this.originalPosition = { x: point.x, y: point.y }; // 記錄原始位置
            this.offsetX = mouseX - point.x;
            this.offsetY = mouseY - point.y;
          }
        });
      }
    },
    handleMouseMove(event) {
      if (this.isDragging && this.draggedPoint) {
        const mouseX = event.offsetX;
        const mouseY = event.offsetY;

        // 更新被拖曳點的座標
        this.draggedPoint.x = mouseX - this.offsetX;
        this.draggedPoint.y = mouseY - this.offsetY;

        this.clearCanvas();
        this.redrawPoints();
      }
    },
handleMouseUp(event) {
  if (event.button === 0) {
    // 當用戶放開滑鼠時，彈出確認對話框
    if (this.isDragging) {
      const confirmPlace = confirm("是否要將點放置在此?");
      if (confirmPlace) {
        // 確認放置，結束拖曳
        this.isDragging = false; // 結束拖曳
        this.originalPosition = null; // 清空原始位置
        // 不需要在這裡更新 draggedPoint，因為它已經在 handleMouseMove 中更新過了
      } else {
        // 取消放置，恢復原始位置
        if (this.draggedPoint && this.originalPosition) {
          this.draggedPoint.x = this.originalPosition.x;
          this.draggedPoint.y = this.originalPosition.y;
          this.clearCanvas();
          this.redrawPoints();
        }
      }
      // 確保清空拖曳的點
      this.isDragging = false;
      this.draggedPoint = null; 
    }
  }
}
,


    confirmAddPoint() {
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
    },
    resetNewPoint() {
      this.newPoint.x = 0;
      this.newPoint.y = 0;
      this.newPoint.tagID = '';
      this.newPoint.tagName = '';
      this.addingPoint = false;
    },
    drawPoint(x, y, color = 'blue') {
      this.context.beginPath();
      this.context.arc(x, y, 3, 0, Math.PI * 2);
      this.context.fillStyle = color;
      this.context.fill();

      const tagID = this.points.find(point => point.x === x && point.y === y)?.tagID;
      if (tagID) {
        this.context.font = '12px Arial';
        this.context.fillStyle = 'black';
        this.context.fillText(`${tagID}`, x + 5, y - 5);
      }
    },
    showPointInfo(mouseX, mouseY) {
      for (const point of this.points) {
        if (Math.abs(point.x - mouseX) <= 3 && Math.abs(point.y - mouseY) <= 3) {
          this.selectedPoint = point;
          return;
        }
      }
      this.selectedPoint = null;
    },
    clearCanvas() {
      this.context.clearRect(0, 0, this.$refs.canvas.width, this.$refs.canvas.height);
    },
    redrawPoints() {
      for (const point of this.points) {
        this.drawPoint(point.x, point.y);
      }
    },
    deletePoint(pointToDelete) {
      this.points = this.points.filter(point => point !== pointToDelete);
      this.selectedPoint = null;
      this.clearCanvas();
      this.redrawPoints();
    },
  }
};
</script>

<style scoped>
button {
  padding: 5px 10px;
  margin: 0 5px;
  cursor: pointer;
  border: 1px solid #ccc;
  background-color: #f0f0f0;
}

button.active {
  background-color: #e0e0e0;
}

canvas {
  border: 1px solid #000;
}

table {
  margin-top: 10px;
  border-collapse: collapse;
}

table, th, td {
  border: 1px solid #ddd;
}

th, td {
  padding: 5px;
  text-align: left;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin-bottom: 10px;
}
</style>
