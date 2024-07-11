<template>
  <div class="app">
    <!-- 點位顯示區域 -->
    <div class="point-container">
      <div v-for="point in points" :key="point.id" 
           class="point" 
           :style="{ top: point.y + 'px', left: point.x + 'px' }" 
           @click="selectPoint(point)">
      </div>
    </div>
    
    <!-- 點位資訊表格區域 -->
    <div v-if="selectedPoint" class="info-table">
      <table>
        <tr>
          <td>Tag_ID</td>
          <td><input v-model="formData.Tag_ID" type="text"/></td>
        </tr>
        <tr>
          <td>Tag_Name</td>
          <td><input v-model="formData.Tag_Name" type="text"/></td>
        </tr>
        <tr>
          <td>X</td>
          <td><input v-model="formData.X" type="text"/></td>
        </tr>
        <tr>
          <td>Y</td>
          <td><input v-model="formData.Y" type="text"/></td>
        </tr>
        <tr>
          <td>樓層</td>
          <td><input v-model="formData.樓層" type="text"/></td>
        </tr>
        <tr>
          <td>樓層編號</td>
          <td><input v-model="formData.樓層編號" type="text"/></td>
        </tr>
        <tr>
          <td>MFG_tag</td>
          <td><input v-model="formData.MFG_tag" type="text"/></td>
        </tr>
        <tr>
          <td>端點架台類型</td>
          <td><input v-model="formData.端點架台類型" type="text"/></td>
        </tr>
        <tr>
          <td>虛擬點位</td>
          <td><input v-model="formData.虛擬點位" type="text"/></td>
        </tr>
      </table>
      <div class="buttons">
        <button @click="cancelEdit">取消</button>
        <button @click="updatePoint">修改</button>
        <button @click="deletePoint">刪除</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MapWeeb',
  data() {
    return {
      points: [
        { id: 1, x: 100, y: 150, Tag_ID: 'T1', Tag_Name: '點位1', X: 100, Y: 150, 樓層: '1F', 樓層編號: '1', MFG_tag: 'MFG1', 端點架台類型: '類型1', 虛擬點位: '虛擬1' },
        { id: 2, x: 200, y: 250, Tag_ID: 'T2', Tag_Name: '點位2', X: 200, Y: 250, 樓層: '2F', 樓層編號: '2', MFG_tag: 'MFG2', 端點架台類型: '類型2', 虛擬點位: '虛擬2' },
        { id: 3, x: 300, y: 350, Tag_ID: 'T3', Tag_Name: '點位3', X: 300, Y: 350, 樓層: '3F', 樓層編號: '3', MFG_tag: 'MFG3', 端點架台類型: '類型3', 虛擬點位: '虛擬3' },
      ],
      selectedPoint: null,
      formData: {
        Tag_ID: '',
        Tag_Name: '',
        X: '',
        Y: '',
        樓層: '',
        樓層編號: '',
        MFG_tag: '',
        端點架台類型: '',
        虛擬點位: ''
      }
    }
  },
  methods: {
    selectPoint(point) {
      this.selectedPoint = point;
      this.formData = { ...point };
    },
    cancelEdit() {
      this.selectedPoint = null;
    },
    updatePoint() {
      if (this.selectedPoint) {
        Object.assign(this.selectedPoint, this.formData);
        this.cancelEdit();
      }
    },
    deletePoint() {
      if (this.selectedPoint) {
        this.points = this.points.filter(point => point.id !== this.selectedPoint.id);
        this.cancelEdit();
      }
    }
  }
}
</script>

<style scoped>
.app {
  display: flex;
  justify-content: center; /* 將內容水平置中 */
  align-items: center; /* 將內容垂直置中 */
  position: relative; /* 加上相對定位，以便設置子元素的絕對定位 */
}

.point-container {
  position: relative;
  width: 500px;
  height: 500px;
  border: 1px solid #ccc;
}

.point {
  position: absolute;
  width: 10px;
  height: 10px;
  background-color: red;
  border-radius: 50%;
  cursor: pointer;
}

.info-table {
  position: absolute;
  left: 410px; /* 調整表格位置，使其顯示在畫布的右側 */
  top: 0;
  width: 250px; /* 調整表格寬度 */
  padding: 10px;
  border: 1px solid #ccc;
  background-color: #f9f9f9;
}

.info-table table {
  width: 100%;
  border-collapse: collapse;
}

.info-table td {
  padding: 8px;
  border: 1px solid #ddd;
}

.info-table input {
  width: calc(100% - 20px);
}

.buttons {
  margin-top: 10px;
}

.buttons button {
  margin-right: 5px;
}
</style>

