<template>
  <div>
    <!-- Mode selection -->
    <div>
      <label>選擇繪圖模式：</label>
      <button :class="{ active: currentMode === 'drawPoint' }" @click="setCurrentMode('drawPoint')">點</button>
      <button :class="{ active: currentMode === 'drawPath' }" @click="setCurrentMode('drawPath')">點路徑</button>
      <button :class="{ active: currentMode === 'clickMode' }" @click="setCurrentMode('clickMode')">點選</button>
    </div>

    <!-- Canvas -->
    <canvas ref="canvas" width="600" height="400"
            @click="handleCanvasClick"
            style="border:1px solid #000;">
      Your browser does not support the HTML5 canvas tag.
    </canvas>

    <!-- Input point info -->
    <div v-if="currentMode === 'drawPoint' && addingPoint">
      <h2>新增點</h2>
      <label for="tag-id">Tag_ID：</label>
      <input type="text" id="tag-id" v-model="newPoint.tagID"><br>

      <label for="tag-name">Tag_Name：</label>
      <input type="text" id="tag-name" v-model="newPoint.tagName"><br>

      <label for="x-coordinate">X 座標：</label>
      <input type="number" id="x-coordinate" v-model.number="newPoint.x"><br>

      <label for="y-coordinate">Y 座標：</label>
      <input type="number" id="y-coordinate" v-model.number="newPoint.y"><br>

      <button @click="confirmAddPoint">確認新增</button>
      <button @click="cancelAddPoint">取消</button>
    </div>

    <!-- Input path info -->
    <div v-if="currentMode === 'drawPath' && pathPoints.length === 2">
      <h2>新增路徑</h2>
      <table>
        <tr>
          <th>起點資訊</th>
          <th>終點資訊</th>
        </tr>
        <tr>
          <td>
            <p><strong>Tag_ID:</strong> {{ pathPoints[0].tagID }}</p>
            <p><strong>起點坐標:</strong> ({{ pathPoints[0].x }}, {{ pathPoints[0].y }})</p>
          </td>
          <td>
            <p><strong>Tag_ID:</strong> {{ pathPoints[1].tagID }}</p>
            <p><strong>終點坐標:</strong> ({{ pathPoints[1].x }}, {{ pathPoints[1].y }})</p>
          </td>
        </tr>
      </table>
      <label for="path-speed">路徑速度：</label>
      <input type="number" id="path-speed" v-model.number="newPath.speed" min="0" step="0.1"><br>

      <button @click="confirmAddPath">確認新增</button>
      <button @click="cancelAddPath">取消</button>
    </div>

    <!-- Display point and path info -->
    <div v-if="selectedPoint || selectedPath" style="margin-top: 10px;">
      <div v-if="selectedPoint">
        <h2>點資訊</h2>
        <p><strong>Tag_ID:</strong> {{ selectedPoint.tagID }}</p>
        <p><strong>X 座標:</strong> {{ selectedPoint.x }}</p>
        <p><strong>Y 座標:</strong> {{ selectedPoint.y }}</p>
        <h3>相關路徑</h3>
        <ul>
          <li v-for="path in getRelatedPaths(selectedPoint)" :key="`${path.start.tagID}-${path.end.tagID}`">
            <p><strong>起點 Tag_ID:</strong> {{ path.start.tagID }}</p>
            <p><strong>終點 Tag_ID:</strong> {{ path.end.tagID }}</p>
            <p><strong>起點坐標:</strong> ({{ path.start.x }}, {{ path.start.y }})</p>
            <p><strong>終點坐標:</strong> ({{ path.end.x }}, {{ path.end.y }})</p>
            <p><strong>路徑速度:</strong> {{ path.speed }}</p>
            <button @click="deletePath(path)">刪除路徑</button>
          </li>
        </ul>
        <!-- 刪除點按鈕 -->
        <button @click="deletePoint(selectedPoint)">刪除點</button>
      </div>

      <div v-if="selectedPath">
        <h2>路徑資訊</h2>
        <p><strong>起點 Tag_ID:</strong> {{ selectedPath.start.tagID }}</p>
        <p><strong>終點 Tag_ID:</strong> {{ selectedPath.end.tagID }}</p>
        <p><strong>起點坐標:</strong> ({{ selectedPath.start.x }}, {{ selectedPath.start.y }})</p>
        <p><strong>終點坐標:</strong> ({{ selectedPath.end.x }}, {{ selectedPath.end.y }})</p>
        <p><strong>路徑速度:</strong> {{ selectedPath.speed }}</p>
        <!-- 刪除路徑按鈕 -->
        <button @click="deletePath(selectedPath)">刪除路徑</button>
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
      currentMode: 'drawPoint',  // Default mode is drawing points
      points: [],  // Array to store clicked points
      selectedPoint: null,  // Store the selected point for displaying info
      addingPoint: false,  // Flag to indicate if adding a new point
      newPoint: {
        x: 0,
        y: 0,
        tagID: '',
        tagName: ''
      },
      pathPoints: [],  // Array to store points for drawing paths
      newPath: {
        endX: 0,
        endY: 0,
        speed: 0
      },
      paths: [],  // Array to store paths
      selectedPath: null  // Store the selected path for displaying info
    };
  },
  mounted() {
    this.context = this.$refs.canvas.getContext('2d');
  },
  methods: {
    setCurrentMode(mode) {
      this.currentMode = mode;
      // Reset any active states or temporary data here if needed
      if (mode !== 'drawPath') {
        this.clearPathPreview();
      }
    },
    handleCanvasClick(event) {
      const mouseX = event.offsetX;
      const mouseY = event.offsetY;

      // Clear previous red point if addingPoint is true
      if (this.addingPoint) {
        this.clearCanvas();
        this.redrawPoints();
        this.redrawPaths();
      }

      if (this.currentMode === 'drawPoint') {
        // Start adding a new point
        this.addingPoint = true;
        this.newPoint.x = mouseX;
        this.newPoint.y = mouseY;

        // Draw the point in red to indicate the position
        this.drawPoint(mouseX, mouseY, 'red');
      } else if (this.currentMode === 'clickMode') {
        // Show point info on click
        this.showPointInfo(mouseX, mouseY);
      } else if (this.currentMode === 'drawPath') {
        this.addPathPoint(mouseX, mouseY);
      }
    },
    confirmAddPoint() {
      // Add the new point to points array
      this.points.push({
        x: this.newPoint.x,
        y: this.newPoint.y,
        tagID: this.newPoint.tagID,
        tagName: this.newPoint.tagName
      });

      // Draw the point on the canvas (in blue as default)
      this.drawPoint(this.newPoint.x, this.newPoint.y);

      // Reset newPoint data and hide input section
      this.resetNewPoint();
    },
    cancelAddPoint() {
      // Clear newPoint data and hide input section
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

      // Display TAG ID next to the point
      const tagID = this.points.find(point => point.x === x && point.y === y)?.tagID;
      if (tagID) {
        this.context.font = '12px Arial';
        this.context.fillStyle = 'black';
        this.context.fillText(`${tagID}`, x + 5, y - 5); // Adjust position as needed
      }
    },
    addPathPoint(mouseX, mouseY) {
      // Check if clicked on an existing point to add to pathPoints
      let clickedPoint = null;
      for (const point of this.points) {
        if (Math.abs(point.x - mouseX) <= 3 && Math.abs(point.y - mouseY) <= 3) {
          clickedPoint = point;
          break;
        }
      }
      if (clickedPoint) {
        this.pathPoints.push({ x: clickedPoint.x, y: clickedPoint.y, tagID: clickedPoint.tagID });

        // If we have exactly two points, show path info and add a new point
        if (this.pathPoints.length === 2) {
          const startPoint = this.pathPoints[0];
          const endPoint = this.pathPoints[1];
          
          // Set the new path end coordinates
          this.newPath.endX = endPoint.x;
          this.newPath.endY = endPoint.y;

          // Draw the path preview (dashed line)
          this.drawDashedLine(startPoint.x, startPoint.y, endPoint.x, endPoint.y);
        }
      }
    },
    confirmAddPath() {
      // Create the path object
      const startPoint = this.pathPoints[0];
      const endPoint = this.pathPoints[1];
      const path = {
        start: startPoint,
        end: endPoint,
        speed: this.newPath.speed
      };

      // Add the path to the paths array
      this.paths.push(path);

      // Clear the path preview and reset pathPoints
      this.clearPathPreview();
      this.pathPoints = [];

      // Clear canvas and redraw all points and paths
      this.clearCanvas();
      this.redrawPoints();
      this.redrawPaths();
    },
    cancelAddPath() {
      // Clear the path preview and reset pathPoints
      this.clearPathPreview();
      this.pathPoints = [];
    },
    clearPathPreview() {
      // Clear the path preview (dashed line)
      this.clearCanvas();
      this.redrawPoints();
      this.redrawPaths();
    },
    drawDashedLine(x1, y1, x2, y2) {
      this.context.beginPath();
      this.context.setLineDash([5, 5]);  // Dashed line pattern
      this.context.moveTo(x1, y1);
      this.context.lineTo(x2, y2);
      this.context.strokeStyle = 'gray';
      this.context.stroke();
      this.context.setLineDash([]);  // Reset to solid line
    },
    showPointInfo(mouseX, mouseY) {
      // Check if clicked on an existing point
      for (const point of this.points) {
        if (Math.abs(point.x - mouseX) <= 3 && Math.abs(point.y - mouseY) <= 3) {
          // Found the clicked point
          this.selectedPoint = point;
          this.selectedPath = null;  // Clear selected path

          // Draw the point in green to indicate selection
          this.clearCanvas();
          this.redrawPoints();
          this.redrawPaths();
          this.drawPoint(point.x, point.y, 'green');
          return;
        }
      }
      // Clicked outside any point, clear selected point and path
      this.selectedPoint = null;
      this.selectedPath = null;
    },
    getRelatedPaths(point) {
      // Get all paths where the given point is the start of the path
      return this.paths.filter(path => 
        path.start.x === point.x && path.start.y === point.y
      );
    },
    deletePoint(pointToDelete) {
      // Filter out the point to delete
      this.points = this.points.filter(point => point !== pointToDelete);

      // Filter out the paths related to the point to delete
      this.paths = this.paths.filter(path => 
        !(path.start.x === pointToDelete.x && path.start.y === pointToDelete.y) &&
        !(path.end.x === pointToDelete.x && path.end.y === pointToDelete.y)
      );

      // Clear selectedPoint and selectedPath since they are deleted
      this.selectedPoint = null;
      this.selectedPath = null;

      // Clear canvas and redraw remaining points and paths
      this.clearCanvas();
      this.redrawPoints();
      this.redrawPaths();
    },
    deletePath(pathToDelete) {
      // Filter out the path to delete
      this.paths = this.paths.filter(path => path !== pathToDelete);

      // Clear selectedPath since it's deleted
      this.selectedPath = null;

      // Clear canvas and redraw remaining points and paths
      this.clearCanvas();
      this.redrawPoints();
      this.redrawPaths();
    },
    clearCanvas() {
      // Clear the canvas
      this.context.clearRect(0, 0, this.$refs.canvas.width, this.$refs.canvas.height);
    },
    redrawPoints() {
      // Redraw all points
      for (const point of this.points) {
        this.drawPoint(point.x, point.y);
      }
    },
    redrawPaths() {
      // Draw all paths
      this.context.beginPath();
      this.context.strokeStyle = 'black';
      this.context.lineWidth = 1;

      for (const path of this.paths) {
        this.drawLine(path.start.x, path.start.y, path.end.x, path.end.y);
      }
    },
    drawLine(x1, y1, x2, y2) {
      this.context.beginPath();
      this.context.moveTo(x1, y1);
      this.context.lineTo(x2, y2);
      this.context.stroke();
    }
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
