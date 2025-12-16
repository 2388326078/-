/**
 * 自定义弹窗系统
 */
class CustomModal {
    constructor() {
        this.modalElement = null;
        this.overlayElement = null;
    }

    /**
     * 创建弹窗HTML结构
     * @param {Object} options - 弹窗配置
     * @returns {HTMLElement} - 弹窗元素
     */
    createModal(options) {
        const { title, message, type = 'alert', onConfirm, onCancel } = options;

        // 创建遮罩层
        this.overlayElement = document.createElement('div');
        this.overlayElement.className = 'modal-overlay';

        // 创建弹窗容器
        this.modalElement = document.createElement('div');
        this.modalElement.className = 'modal';

        // 创建弹窗头部
        const header = document.createElement('div');
        header.className = 'modal-header';

        const modalTitle = document.createElement('h3');
        modalTitle.className = 'modal-title';
        modalTitle.textContent = title;

        const closeBtn = document.createElement('button');
        closeBtn.className = 'modal-close';
        closeBtn.innerHTML = '&times;';
        closeBtn.addEventListener('click', () => this.close());

        header.appendChild(modalTitle);
        header.appendChild(closeBtn);

        // 创建弹窗内容
        const body = document.createElement('div');
        body.className = 'modal-body';
        body.textContent = message;

        // 创建弹窗底部
        const footer = document.createElement('div');
        footer.className = 'modal-footer';

        // 创建按钮
        if (type === 'confirm') {
            const cancelBtn = document.createElement('button');
            cancelBtn.className = 'modal-btn modal-btn-secondary';
            cancelBtn.textContent = '取消';
            cancelBtn.addEventListener('click', () => {
                this.close();
                if (onCancel) onCancel();
            });
            footer.appendChild(cancelBtn);
        }

        const confirmBtn = document.createElement('button');
        confirmBtn.className = 'modal-btn modal-btn-primary';
        confirmBtn.textContent = '确认';
        confirmBtn.addEventListener('click', () => {
            this.close();
            if (onConfirm) onConfirm();
        });
        footer.appendChild(confirmBtn);

        // 组装弹窗
        this.modalElement.appendChild(header);
        this.modalElement.appendChild(body);
        this.modalElement.appendChild(footer);
        this.overlayElement.appendChild(this.modalElement);

        // 添加到文档
        document.body.appendChild(this.overlayElement);

        // 添加键盘事件
        document.addEventListener('keydown', this.handleKeyDown.bind(this));

        // 添加点击遮罩层关闭事件
        this.overlayElement.addEventListener('click', (e) => {
            if (e.target === this.overlayElement) {
                this.close();
            }
        });

        return this.modalElement;
    }

    /**
     * 显示弹窗
     * @param {Object} options - 弹窗配置
     */
    show(options) {
        this.createModal(options);
        // 触发动画
        setTimeout(() => {
            this.overlayElement.classList.add('active');
        }, 10);
    }

    /**
     * 关闭弹窗
     */
    close() {
        if (this.overlayElement) {
            this.overlayElement.classList.remove('active');
            // 等待动画结束后移除元素
            setTimeout(() => {
                this.overlayElement.remove();
                this.overlayElement = null;
                this.modalElement = null;
            }, 300);
        }
        // 移除键盘事件
        document.removeEventListener('keydown', this.handleKeyDown.bind(this));
    }

    /**
     * 处理键盘事件
     * @param {KeyboardEvent} e - 键盘事件
     */
    handleKeyDown(e) {
        if (e.key === 'Escape') {
            this.close();
        }
    }
}

// 全局弹窗实例
const customModal = new CustomModal();

/**
 * 自定义alert弹窗
 * @param {string} message - 弹窗消息
 * @param {string} title - 弹窗标题
 * @param {Function} onConfirm - 确认回调
 */
function customAlert(message, title = '提示', onConfirm) {
    customModal.show({
        title,
        message,
        type: 'alert',
        onConfirm
    });
}

/**
 * 自定义confirm弹窗
 * @param {string} message - 弹窗消息
 * @param {string} title - 弹窗标题
 * @param {Function} onConfirm - 确认回调
 * @param {Function} onCancel - 取消回调
 */
function customConfirm(message, title = '确认', onConfirm, onCancel) {
    customModal.show({
        title,
        message,
        type: 'confirm',
        onConfirm,
        onCancel
    });
}

/**
 * 公共JS函数：表单提交确认提示
 * @param {Event} e - 表单提交事件
 * @param {string} message - 确认提示信息
 */
function confirmSubmit(e, message = "确定要提交吗？") {
    e.preventDefault(); // 先阻止默认提交
    customConfirm(message, '提交确认', () => {
        e.target.submit(); // 确认后手动提交
    });
}

/**
 * 公共JS函数：删除操作确认提示
 * @param {Event} e - 点击事件
 * @param {string} message - 确认提示信息
 */
function confirmDelete(e, message = "确定要删除吗？删除后数据不可恢复！") {
    e.preventDefault(); // 先阻止默认跳转
    const href = e.currentTarget.href;
    customConfirm(message, '删除确认', () => {
        window.location.href = href; // 确认后跳转
    });
}

/**
 * 公共JS函数：简单的表单验证（非空验证）
 * @param {HTMLFormElement} form - 表单元素
 * @param {Array} requiredFields - 必选字段的name属性数组
 * @returns {boolean} - 验证通过返回true，否则返回false
 */
function validateForm(form, requiredFields) {
    let isValid = true;
    requiredFields.forEach(fieldName => {
        const field = form.querySelector(`[name="${fieldName}"]`);
        if (field) {
            const value = field.value.trim();
            if (value === "") {
                customAlert(`"${field.previousElementSibling.textContent.replace('：', '').replace('*', '')}" 不能为空！`);
                field.focus();
                isValid = false;
                return false; // 终止forEach循环
            }
        }
    });
    return isValid;
}

/**
 * 公共JS函数：渲染表格数据（模拟后端数据渲染，实际项目中由后端传值）
 * @param {string} tableId - 表格ID
 * @param {Array} data - 数据数组
 * @param {Array} columns - 列配置：[{key: '字段名', label: '列名'}]
 */
function renderTable(tableId, data, columns) {
    const table = document.getElementById(tableId);
    if (!table) return;

    // 清空表格内容（保留表头）
    const tbody = table.querySelector("tbody");
    tbody.innerHTML = "";

    if (data.length === 0) {
        const tr = document.createElement("tr");
        const td = document.createElement("td");
        td.colSpan = columns.length;
        td.textContent = "暂无数据";
        td.style.textAlign = "center";
        tr.appendChild(td);
        tbody.appendChild(tr);
        return;
    }

    // 渲染数据行
    data.forEach(item => {
        const tr = document.createElement("tr");
        columns.forEach(column => {
            const td = document.createElement("td");
            // 处理特殊数据（如图片）
            if (column.key === "photo" && item[column.key]) {
                const img = document.createElement("img");
                img.src = item[column.key];
                img.alt = "照片";
                td.appendChild(img);
            } else {
                td.textContent = item[column.key] || "无";
            }
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });
}

// 页面加载完成后执行
document.addEventListener("DOMContentLoaded", function() {
    // 为所有带data-confirm的表单添加提交确认
    const forms = document.querySelectorAll("form[data-confirm]");
    forms.forEach(form => {
        form.addEventListener("submit", function(e) {
            const message = this.getAttribute("data-confirm") || "确定要提交吗？";
            confirmSubmit(e, message);
        });
    });

    // 为所有带data-delete的链接添加删除确认
    const deleteLinks = document.querySelectorAll("a[data-delete]");
    deleteLinks.forEach(link => {
        link.addEventListener("click", function(e) {
            const message = this.getAttribute("data-delete") || "确定要删除吗？";
            confirmDelete(e, message);
        });
    });
});