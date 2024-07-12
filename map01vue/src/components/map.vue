<template>
  <div class="app">
    <!-- 點位資訊表格區域 -->
    <div v-if="selectedPoint" class="info-table">
      <table class="custom-table">
        <tr style="background-color: #0E356E;">
          <td colspan="2" style="color: white; text-align: center; padding: 10px; border-radius: 8px; font-weight: bold; font-size: 18px;">點位資訊</td>
        </tr>
        <tr>
          <td style="width: 200px;">Tag_ID</td>
          <td><input v-model="formData.Tag_ID" type="text" style="width: 160px;" /></td>
        </tr>
        <tr>
          <td style="width: 200px;">Tag_Name</td>
          <td><input v-model="formData.Tag_Name" type="text" style="width: 160px;" /></td>
        </tr>
        <tr>
          <td style="width: 200px;">X</td>
          <td><input v-model="formData.X" type="text" style="width: 160px;" /></td>
        </tr>
        <tr>
          <td style="width: 200px;">Y</td>
          <td><input v-model="formData.Y" type="text" style="width: 160px;" /></td>
        </tr>
        <tr>
          <td style="width: 200px;">樓層</td>
          <td><input v-model="formData.floor" type="text" style="width: 160px;" /></td>
        </tr>
        <tr>
          <td style="width: 200px;">樓層編號</td>
          <td><input v-model="formData.floorID" type="text" style="width: 160px;" /></td>
        </tr>
        <tr>
          <td style="width: 200px;">MFG_tag</td>
          <td><input v-model="formData.MFG_tag" type="text" style="width: 160px;" /></td>
        </tr>
        <tr>
          <td style="width: 200px;">端點架台類型</td>
          <td><input v-model="formData.Endpoint" type="text" style="width: 160px;" /></td>
        </tr>
        <tr>
          <td style="width: 200px;">虛擬點位</td>
          <td><input v-model="formData.virtual" type="text" style="width: 160px;" /></td>
        </tr>
      </table>
      <div class="buttons">
        <button class="btn btn-cancel" @click="cancelEdit">取消修改</button>
        <button class="btn btn-update" @click="updatePoint">修改點</button>
        <button class="btn btn-delete" @click="deletePoint">刪除點</button>
      </div>
    </div>
<br>s
    <!-- 路徑資訊表格區域 -->
    <div v-if="selectedPoint" class="info-table">
      <table class="custom-table">
        <tr style="background-color: #0E356E;">
          <td colspan="2" style="color: white; text-align: center; padding: 10px; border-radius: 8px; font-weight: bold; font-size: 18px;">路徑資訊</td>
        </tr>
        <tr>
          <td style="width: 200px;">Tag_ID</td>
          <td><input v-model="formData.Tag_ID" type="text" style="width: 160px;" /></td>
        </tr>
        <tr>
          <td style="width: 200px;">順行方向與障礙物</td>
          <td><input v-model="formData.Tag_Name" type="text" style="width: 160px;" /></td>
        </tr>
        <tr>
          <td style="width: 200px;">順行速度</td>
          <td><input v-model="formData.X" type="text" style="width: 160px;" /></td>
        </tr>
        <tr>
          <td style="width: 200px;">逆行方向與障礙物</td>
          <td><input v-model="formData.Y" type="text" style="width: 160px;" /></td>
        </tr>
        <tr>
          <td style="width: 200px;">逆行方向</td>
          <td><input v-model="formData.floor" type="text" style="width: 160px;" /></td>
        </tr>
        <tr>
          <td style="width: 200px;">車種</td>
          <td><input v-model="formData.floorID" type="text" style="width: 160px;" /></td>
        </tr>
        <tr>
          <td style="width: 200px;">距離 (cm)</td>
          <td><input v-model="formData.MFG_tag" type="text" style="width: 160px;" /></td>
        </tr>
        <tr>
          <td style="width: 200px;">板車退後</td>
          <td><input v-model="formData.Endpoint" type="text" style="width: 160px;" /></td>
        </tr>
        <tr>
          <td style="width: 200px;">虛擬點位</td>
          <td><input v-model="formData.virtual" type="text" style="width: 160px;" /></td>
        </tr>
      </table>
      <div class="buttons">
        <button class="btn btn-cancel" @click="cancelEdit">取消修改</button>
        <button class="btn btn-update" @click="updatePoint">修改路徑</button>
        <button class="btn btn-delete" @click="deletePoint">刪除路徑</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MapWeeb',
  data() {
    return {
      selectedPoint: true,
      formData: {
        Tag_ID: '4322',
        Tag_Name: '4322',
        X: '100',
        Y: '100',
        floor: '4',
        floorID: '4F',
        MFG_tag: '0',
        Endpoint: '0',
        virtual: '0'
      }
    }
  },
  methods: {
    cancelEdit() {
      // 取消編輯的方法
      // 可以重設 formData 到原始資料，或是其他操作
    },
    updatePoint() {
      // 修改點位的方法
      // 可以透過 API 或其他方法更新後端資料
    },
    deletePoint() {
      // 刪除點位的方法
      // 可以透過 API 或其他方法刪除後端資料
    }
  }
}
</script>

<style scoped>
.app {
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

.info-table {
  width: 350px;
  background-color: #0E356E;
  padding: 15px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.custom-table {
  width: 100%;
  border-collapse: collapse;
}

.custom-table td {
  padding: 5px;
  color: white;
  font-weight: bold;
}

.custom-table tr:first-child td {
  border-bottom: none;
  padding-top: 0; /* Remove top padding specifically for the first row */
}

.custom-table input {
  font-size: 16px;
}

.buttons {
  margin-top: 15px;
  text-align: center;
}

.btn {
  padding: 8px 15px;
  margin: 0 10px;
  font-size: 16px;
  font-weight: bold;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-cancel {
  background-color: #4CAF50;
  color: white;
}

.btn-update {
  background-color: #FFC107;
  color: white;
}

.btn-delete {
  background-color: #F44336;
  color: white;
}

.btn:hover {
  opacity: 0.8;
}
</style>
