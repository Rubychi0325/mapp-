<template>

  <section class="untitled-page mainSection">
    <!-- Main Section -->

    <img class="mainImage" src="/assets/c04313638dc386f9db4b6b9c9d4272f9.png" alt="alt text" />
    <section class="contentSection">
      <!-- Content Section -->

      <div class="titleContainer">
        <!-- Title container -->

        <h2 class="mediumTitle">●</h2>
        <h2 class="mediumTitle1">＼</h2>
        <img class="subImage" src="/assets/3e0dade52bc061b599701a6dfe360f98.svg" alt="alt text" />
      </div>
      <section class="locationDetails">
        <!-- Location Details Section -->

        <header class="locationHeader">
          <!-- Header for location details -->

          <span class="highlightText1">廠區：</span>
          <span class="highlightText2">AGV</span>
        </header>
        <div class="contentBox1">
          <!-- Content box -->

          <div class="rectangle"></div>
        </div>
      </section>

    </section>

    <div class="rect"></div>
    <section class="infoSection">
      <!-- Information Section -->

      <section class="infoGrid">
        <!-- Information Grid -->

        <div class="gridContainer">
          <!-- Grid Container -->

          <div class="gridItem">
            <h3 class="infoHeader">點位資訊</h3>
            <div class="flexRow">
              <p class="highlightText11">Tag_ID</p>
              <p class="highlightText21"></p>
            </div>
            <div class="flexRow1">
              <p class="highlightText12">Tag_Name</p>
              <p class="highlightText21"></p>
            </div>
            <div class="flexRow2">
              <p class="highlightText11">X</p>
              <p class="highlightText21"></p>
            </div>
            <div class="flexRow2">
              <p class="highlightText11">Y</p>
              <p class="highlightText21"></p>
            </div>
            <div class="flexRow3">
              <p class="highlightText11">樓層</p>
              <p class="highlightText21"></p>
            </div>
            <div class="flexRow4">
              <p class="highlightText12">樓層編號</p>
              <p class="highlightText21"></p>
            </div>
            <div class="flexRow5">
              <p class="highlightText12">MFG_tag</p>
              <p class="highlightText21"></p>
            </div>
            <div class="flexRow6">
              <p class="highlightText12">端點架台類型</p>
              <div class="rectangle2"></div>
            </div>
            <div class="flexRow7">
              <p class="highlightText12">虛擬點位</p>
              <div class="contentBox"></div>
            </div>
          </div>
          <button class="modifyButton">
            <!-- TODO -->
             修改
          </button>
          <button class="cancelButton">
            <!-- TODO -->
             取消
          </button>
          <button class="deleteButton">
            <!-- TODO -->
             刪除點
          </button>
        </div>
      </section>

    </section>

  </section>

</template>

<script>
export default {
  name: 'MapWebb',
};
</script>

<style scoped lang="scss">
@use "./utils.scss" as *;
@use "./global.scss" as *;

.untitled-page {
  &.mainSection {
    position: relative;
    display: flex;
    flex-direction: column;
    background-color: rgb(255 255 255);
    overflow: hidden;
  }

  .mainImage {
    position: absolute;
    top: 288px;
    left: 682px;
    width: 25px;
    height: 20px;
    aspect-ratio: 1.25;
  }

  .contentSection {
    position: relative;
    display: flex;
    flex-direction: column;
    gap: 25px 0;
    margin: 360px 18px 58px auto;
    width: 205px;
    max-width: 85%;

    @include md {
      margin: 150px 18px 58px auto;
    }

    @include xs {
      margin: 80px 16px 58px auto;
    }

    @include tn {
      margin: 50px 8px 50px auto;
    }
  }

  .titleContainer {
    display: flex;
    flex-direction: column;
    gap: 11px 0;
    margin: 0 0 0 auto;
    width: 35px;
  }

  .mediumTitle {
    font: 700 24px/1.2 Inter, Helvetica, Arial, serif;
    color: rgb(255 255 255);
    background: url("placeholder.png") center
      center / cover no-repeat;
    padding: 3px 7px;

    @include md {
      align-items: flex-start;
      font-size: 22px;
    }

    @include xxs {
      font-size: 20px;
    }
  }

  .mediumTitle1 {
    display: flex;
    justify-content: center;
    font: 900 24px/1.2 Inter, Helvetica, Arial, serif;
    color: rgb(255 255 255);
    text-align: center;
    background-color: rgb(14 53 110);
    border-radius: 6px;
    padding: 3px 4px;
    outline: 0.20000000298023224px solid rgb(0 38 173);
    outline-offset: -0.20000000298023224px;
    box-shadow: 2px 2px 2px 0 rgb(0 0 0 / 24.7%);

    @include md {
      align-items: flex-start;
      font-size: 22px;
    }

    @include xxs {
      font-size: 20px;
    }
  }

  .subImage {
    width: 35px;
    height: 35px;
    object-fit: cover;
  }

  .locationDetails {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 9px 0;
  }

  .locationHeader {
    display: flex;
    gap: 0 5px;
    width: 90.24%;
  }

  .highlightText1 {
    font: 700 16px/1.18 Inter, Helvetica, Arial, serif;
    color: rgb(14 53 110);
  }

  .highlightText2 {
    font: 700 16px/1.18 Inter, Helvetica, Arial, serif;
    color: rgb(14 53 110);
  }

  .contentBox1 {
    display: flex;
    flex-direction: column;
    width: 100%;
    background: url("street-map.png") center
      center / cover no-repeat;
    outline: 1px solid rgb(171 171 171);
    outline-offset: -1px;
    filter: drop-shadow(0 4px 4px rgb(0 0 0 / 24.7%));
  }

  .rectangle {
    margin: 18px 0 61px 24px;
    width: 74px;
    max-width: 85%;
    min-height: 43px;
    background-color: rgb(255 180 180 / 35.6%);
    outline: 1px solid rgb(212 166 166);
    outline-offset: -1px;

    @include xs {
      margin: 18px 0 61px 16px;
    }

    @include tn {
      margin: 18px 0 50px 8px;
    }
  }

  .rect {
    position: absolute;
    bottom: 0;
    left: 50%;
    width: 1280px;
    height: 36px;
    background-color: rgb(14 53 110);
    border-radius: 4px;
    transform: translate(-50%, 0);
  }

  .infoSection {
    position: absolute;
    top: 19px;
    left: 24px;
    display: flex;
    flex-direction: column;
    width: 324px;
    height: 341px;
    background-color: rgb(14 53 111);
    border-radius: 20px;
    box-shadow: 2px 4px 4px 0 rgb(0 0 0 / 24.7%);
  }

  .infoGrid {
    display: flex;
    flex-direction: column;
    margin: 12px 30px 13px 21px;

    @include xs {
      margin: 12px 16px 13px;
    }

    @include tn {
      margin: 12px 8px 13px;
    }
  }

  .gridContainer {
    display: grid;
    align-content: start;
    gap: 11px 18px;
    grid-template-columns: repeat(3, minmax(0, 1fr));

    @include xs {
      column-gap: 16px;
    }

    @include tn {
      column-gap: 8px;
    }
  }

  .gridItem {
    display: flex;
    flex-direction: column;
    grid-row: span 1;
    grid-column: span 3;
  }

  .infoHeader {
    display: flex;
    justify-content: center;
    margin: 0 0 0 36.63%;
    width: 64px;
    max-width: 85%;
    font: 700 16px/1.18 Inter, Helvetica, Arial, serif;
    color: rgb(255 255 255);
    text-align: center;
  }

  .flexRow {
    display: flex;
    gap: 0 19px;
    margin: 13px 0 0;

    @include xs {
      column-gap: 16px;
    }

    @include tn {
      column-gap: 8px;
    }
  }

  .highlightText11 {
    width: 96px;
    font: 700 16px/1.18 Inter, Helvetica, Arial, serif;
    color: rgb(255 255 255);
  }

  .highlightText21 {
    width: 158px;
    min-height: 19px;
    background-color: rgb(217 217 217);
    padding: 0 5px;
  }

  .flexRow1 {
    display: flex;
    justify-content: space-between;
    gap: 0 10px;
    margin: 9px 0 0;

    @include tn {
      column-gap: 8px;
    }
  }

  .highlightText12 {
    font: 700 16px/1.18 Inter, Helvetica, Arial, serif;
    color: rgb(255 255 255);
  }

  .flexRow2 {
    display: flex;
    gap: 0 19px;
    margin: 9px 0 0;

    @include xs {
      column-gap: 16px;
    }

    @include tn {
      column-gap: 8px;
    }
  }

  .flexRow3 {
    display: flex;
    gap: 0 19px;
    margin: 9px 0 0;

    @include xs {
      column-gap: 16px;
    }

    @include tn {
      column-gap: 8px;
    }
  }

  .flexRow4 {
    display: flex;
    justify-content: space-between;
    gap: 0 10px;
    margin: 9px 0 0;

    @include tn {
      column-gap: 8px;
    }
  }

  .flexRow5 {
    display: flex;
    justify-content: space-between;
    gap: 0 10px;
    margin: 9px 0 0;

    @include tn {
      column-gap: 8px;
    }
  }

  .flexRow6 {
    display: flex;
    gap: 0 19px;
    margin: 9px 0 0;

    @include xs {
      column-gap: 16px;
    }

    @include tn {
      column-gap: 8px;
    }
  }

  .rectangle2 {
    width: 158px;
    min-height: 19px;
    background-color: rgb(217 217 217);
  }

  .flexRow7 {
    display: flex;
    justify-content: space-between;
    gap: 0 10px;
    margin: 11px 0 0;

    @include tn {
      column-gap: 8px;
    }
  }

  .contentBox {
    width: 158px;
    min-height: 19px;
    background-color: rgb(217 217 217);
  }

  .modifyButton {
    display: flex;
    justify-content: center;
    grid-row: span 1;
    grid-column: span 1;
    font: 700 16px/1.18 Inter, Helvetica, Arial, serif;
    color: rgb(255 255 255);
    text-align: center;
    background-color: rgb(52 199 89);
    border-radius: 6px;
    padding: 4.5px 22px;
    outline: 0.20000000298023224px solid rgb(54 105 67);
    outline-offset: -0.20000000298023224px;
    box-shadow: 2px 2px 2px 0 rgb(0 0 0 / 24.7%);
  }

  .cancelButton {
    display: flex;
    justify-content: center;
    grid-row: span 1;
    grid-column: span 1;
    font: 700 16px/1.18 Inter, Helvetica, Arial, serif;
    color: rgb(255 255 255);
    text-align: center;
    background-color: rgb(255 204 0);
    border-radius: 6px;
    padding: 4.5px 22px;
    outline: 0.20000000298023224px solid rgb(173 139 0);
    outline-offset: -0.20000000298023224px;
    box-shadow: 2px 2px 2px 0 rgb(0 0 0 / 24.7%);
  }

  .deleteButton {
    display: flex;
    justify-content: center;
    grid-row: span 1;
    grid-column: span 1;
    font: 700 16px/1.18 Inter, Helvetica, Arial, serif;
    color: rgb(255 255 255);
    text-align: center;
    background-color: rgb(255 59 48);
    border-radius: 6px;
    padding: 4.5px 14px;
    outline: 0.20000000298023224px solid rgb(208 0 0);
    outline-offset: -0.20000000298023224px;
    box-shadow: 2px 2px 2px 0 rgb(0 0 0 / 24.7%);
  }
}

//@import '@/components/PartialCode.scss';  // Ensure this path is correct
</style>
