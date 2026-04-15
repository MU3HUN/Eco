<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryForm" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="公司" prop="gongsi">
        <el-input v-model="queryParams.gongsi" placeholder="请输入公司名称" clearable size="small" @keyup.enter.native="handleQuery" />
      </el-form-item>
      <el-form-item label="日期" prop="querycxdate">
        <el-date-picker v-model="queryParams.querycxdate" type="daterange" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期">
        </el-date-picker>
      </el-form-item>
      <el-form-item label="是否已验" prop="boolcheck">
        <el-select v-model="queryParams.boolcheck" placeholder="请选择">
          <el-option label="全部" value="-1"> </el-option>
          <el-option label="已验" value="1"> </el-option>
          <el-option label="未验" value="0">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="结果" prop="VerifyMessage">
        <el-select v-model="queryParams.VerifyMessage" placeholder="请选择">
          <el-option label="全部" value="-1"> </el-option>
          <el-option label="真" value="查验成功发票一致"> </el-option>
          <el-option label="假" value="所查发票不存在">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" size="mini" @click="handleQuery">搜索</el-button>
        <el-tooltip class="item" effect="dark" content="把对应文件夹下的发票图片自动识别到数据库" placement="top-end">
          <el-button v-hasPermi="['system:dict:type:post']" type="primary" plain icon="el-icon-picture-outline" size="mini" @click="handleAddinvoinceInfoByOrc">ORC自动识别</el-button>
        </el-tooltip>
        <el-button v-hasPermi="['system:dict:type:{id}:add']" type="primary" plain icon="el-icon-add" size="mini" @click="handleAdd()">添加</el-button>
        <el-button v-hasPermi="['system:dict:type:{id}:delete']" type="danger" plain icon="el-icon-delete" size="mini" :disabled="multiple" @click="handleDelete">删除</el-button>
        <el-tooltip class="item" effect="dark" content="勾选需要验证的发票进行自动识别真假" placement="top-end">
          <el-button v-hasPermi="['system:dict:type:post']" type="primary" plain icon="el-icon-view" size="mini" @click="handleCheckinvoince">发票验真</el-button>
        </el-tooltip>
        <el-tooltip class="item" effect="dark" content="清空文件夹下所有发票图像" placement="top-end">
          <el-button v-hasPermi="['system:dict:type:{id}:delete']" type="danger" plain icon="el-icon-delete" size="mini"  @click="handleClearFiles">清空文件</el-button>
        </el-tooltip>

      </el-form-item>
    </el-form>

    <el-table v-loading="loading" :data="list" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="ID" align="center" prop="id" width="50" />
      <el-table-column label="公司" align="center" prop="gongsi" width="200" />
      <el-table-column label="发票编号" align="center" prop="number" width="100" />
      <el-table-column label="发票代码" align="center" prop="daima" width="100" />
      <el-table-column label="金额" align="center" prop="amount" width="100" />
      <el-table-column label="日期" align="center" prop="ymd" width="100" />
      <el-table-column label="创建时间" align="center" prop="create_datetime" width="180">

        <template slot-scope="scope">
          <span>{{ parseTime(scope.row.create_datetime) }}</span>
        </template>
      </el-table-column>
      <el-table-column label="结果" align="center" prop="create_datetime" width="180">
        <el-table-column label="验真结果" align="center" prop="VerifyMessage" />
        <el-table-column label="是否已验证" align="center" prop="boolcheck" />
        <el-table-column label="更新时间" align="center" prop="update_datetime" />
      </el-table-column>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <el-button v-hasPermi="['system:dict:type:{id}:edit']" size="mini" type="text" icon="el-icon-edit" @click="handleUpdate(scope.row)">编辑</el-button>
          <el-button v-hasPermi="['system:dict:type:{id}:delete']" size="mini" type="text" icon="el-icon-delete" @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="queryParams.pageNum" :limit.sync="queryParams.pageSize" @pagination="getList" />

    <!-- 编辑 -->
    <el-dialog title="编辑" :visible.sync="open" width="800px" append-to-body :close-on-click-modal="false">
      <el-form ref="form" :model="form" :rules="rules" label-width="80px">
        <el-row>
          <el-col :span="12">
            <el-form-item label="发票编号" prop="number">
              <el-input placeholder="发票编号" v-model="form.number">
              </el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="发票代码" prop="daima">
              <el-input placeholder="发票代码" v-model="form.daima">
              </el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item label="金额" prop="amount">
              <el-input-number v-model="form.amount" placeholder="金额" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="日期" prop="ymd">
              <el-input placeholder="日期" v-model="form.ymd">
              </el-input>
            </el-form-item>
          </el-col>
        </el-row>

      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submitForm">确 定</el-button>
        <el-button @click="cancel">取 消</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import {
  getinvoiceinfoList,
  AddinvoinceInfoByOrc,
  Checkinvoince,
  Delinvoince,
  editinvoice,
  addinvoice,
  delfile
} from "@/api/invoice/invoiceinfo";
import moment from "moment";
export default {
  name: "Orc",
  data() {
    return {
      list: [],
      loading: true,
      // 总条数
      total: 0,
      queryParams: {
        pageNum: 1,
        pageSize: 10,
        gongsi: null,
        startDate: null,
        endDate: null,
        boolcheck: null,
        VerifyMessage: null,
      },
      // 选中数组
      ids: [],
      single: true,
      // 非多个禁用
      multiple: true,
      //编辑窗口
      open: false,
      // 表单参数
      form: {},
      // 表单校验
      rules: {
        number: [
          { required: true, message: "发票编号不能为空", trigger: "blur" },
          { min: 8, max: 8, message: "长度8位", trigger: "blur" },
        ],
        daima: [
          { required: true, message: "发票代码不能为空", trigger: "blur" },
          { min: 10, max: 10, message: "长度10位", trigger: "blur" },
        ],
        amount: [
          { required: true, message: "发票代码不能为空", trigger: "blur" },
        ],
        ymd: [
          { required: true, message: "日期不能为空", trigger: "blur" },
          { min: 8, max: 8, message: "长度8位的日期格式", trigger: "blur" },
        ],
      },
      // 显示搜索条件
      showSearch: true,
    };
  },
  created() {
    this.getList();
  },
  methods: {
    handleAddinvoinceInfoByOrc() {
      const loading = this.$loading({
        lock: true,
        text: "Loading",
        spinner: "el-icon-loading",
        background: "rgba(0, 0, 0, 0.7)",
      });
      AddinvoinceInfoByOrc()
        .then((response) => {
          console.log(response);
          if (response.code == 200) {
            this.msgSuccess(response.msg);
            this.getList();
          }
          loading.close();
        })
        .catch((err) => {
          loading.close();
        });
    },
    getList() {
      this.loading = true;
      getinvoiceinfoList(this.queryParams).then((response) => {
        // console.log(response);
        this.list = response.data.list;
        this.total = response.data.total;
        this.loading = false;
      });
    },
    //发票验真
    handleCheckinvoince(row) {
      const loading = this.$loading({
        lock: true,
        text: "Loading",
        spinner: "el-icon-loading",
        background: "rgba(0, 0, 0, 0.7)",
      });
      const ids = row.id || this.ids;
      Checkinvoince(ids)
        .then((response) => {
          // console.log(response);
          if (response.code == 200) {
            this.msgSuccess(response.msg);
            this.getList();
          }
          loading.close();
        })
        .catch((err) => {
          loading.close();
        });
    },
    // 多选框选中数据
    handleSelectionChange(selection) {
      this.ids = selection.map((item) => item.id);
      this.single = selection.length !== 1;
      this.multiple = !selection.length;
    },
    /** 删除按钮操作 */
    handleDelete(row) {
      const ids = row.id || this.ids;
      this.$confirm('是否确认删除字典编号为"' + ids + '"的数据项?', "警告", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(function () {
          return Delinvoince(ids);
        })
        .then(() => {
          this.getList();
          this.msgSuccess("删除成功");
        });
    },
    /** 修改按钮操作 */
    handleUpdate(row) {
      this.reset();
      this.form = row;
      this.open = true;
    },
    /** 添加按钮 */
    handleAdd() {
      this.reset();
      this.open = true;
    },
    /** 提交按钮 */
    submitForm() {
      this.$refs["form"].validate((valid) => {
        if (valid) {
          if (this.form.id != null) {
            editinvoice(this.form).then((response) => {
              this.msgSuccess("修改成功");
              this.open = false;
              this.getList();
            });
          } else {
            addinvoice(this.form).then((response) => {
              this.msgSuccess("新增成功");
              this.open = false;
              this.getList();
            });
          }
        }
      });
    },
    // 取消按钮
    cancel() {
      this.open = false;
      this.reset();
    },
    // 表单重置
    reset() {
      this.form = {
        id: null,
        number: null,
        daima: null,
        amount: null,
        ymd: null,
      };
      this.resetForm("form");
    },
    /** 搜索按钮操作 */
    handleQuery() {
      if (this.queryParams.querycxdate != null) {
        this.queryParams.startDate = this.queryParams.querycxdate[0];
        this.queryParams.endDate = this.queryParams.querycxdate[1];
        this.queryParams.startDate = this.dataFormat(
          this.queryParams.startDate
        );
        this.queryParams.endDate = this.dataFormat(this.queryParams.endDate);
      } else {
        this.queryParams.startDate = null;
        this.queryParams.endDate = null;
      }

      this.queryParams.pageNum = 1;
      this.getList();
    },
    dataFormat(time) {
      return moment(time).format("YYYY-MM-DD");
    },
        /** 清空图像 */
    handleClearFiles() {
      this.$confirm('是否确认清空文件夹?', "警告", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(function () {
          return delfile();
        })
        .then(() => {
         
          this.msgSuccess("清空成功");
        });
    },
  },
};
</script>
