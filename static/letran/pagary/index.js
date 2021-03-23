"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var ElectricComsumption = /** @class */ (function () {
    function ElectricComsumption(energy, times, Ib, n, Ub) {
        if (Ib === void 0) { Ib = 28; }
        if (n === void 0) { n = .8; }
        if (Ub === void 0) { Ub = 72; }
        this.energy = 185; // kW consumidos mensualmente
        this.times = 10; // Cantidad de veces al mes que se carga la moto 
        this.n = .8; // Eficiencia del cargador
        this.Ub = 72; // Tensión de la batería
        this.Ib = 28; // Corriente de la batería
        if (energy <= 0) {
            throw new RangeError('La energía debe ser mayor que 0');
        }
        else if (energy > 10000) {
            throw new RangeError('EL valor de energía es excesivo');
        }
        else {
            this.energy = energy;
        }
        if (times <= 0) {
            throw new RangeError('La cantidad de cargas debe ser mayor que 0');
        }
        else if (times > 100) {
            throw new RangeError('La cantidad de cargas es excesiva');
        }
        else {
            this.times = times;
        }
        if (Ib <= 0) {
            throw new RangeError('La corriente debe ser mayor que 0');
        }
        else if (Ib > 200) {
            throw new RangeError('La corriente es excesiva');
        }
        else {
            this.Ib = Ib;
        }
        if (n <= 0.0) {
            throw new RangeError('La eficiencia debe ser mayor que 0');
        }
        else if (n > 1.) {
            throw new RangeError('La eficiencia es excesiva');
        }
        else {
            this.n = n;
        }
        if (Ub < 23) {
            throw new RangeError('La tensión no se corresponde a un valor estandar');
        }
        else if (n > 72) {
            throw new RangeError('La tensión es excesiva');
        }
        else {
            this.Ub = Ub;
        }
    }
    ElectricComsumption.prototype.calculatePb = function () {
        return this.Ub * this.Ib / (this.n * 1000);
    };
    ElectricComsumption.prototype.calculateCost = function (energy) {
        if (energy === void 0) { energy = this.energy; }
        var tarifa = [.33, 1.07, 1.43, 2.46, 3.0, 4.0, 5.0, 6.0, 7.0, 9.2, 9.45, 9.85, 10.8, 11.8, 12.9, 13.95, 15.0, 20.0];
        var maxComsumption = [100, 150, 200, 250, 300, 350, 400, 450, 500, 600, 700, 1000, 1800, 2600, 3400, 4200, 5000, 10000];
        if (energy > 100) {
            var t_1 = maxComsumption.filter(function (i) { return i < energy; });
            var rest = energy - t_1.reverse()[0];
            t_1.reverse();
            t_1 = t_1.map(function (i, index) {
                if (index > 0) {
                    return (t_1[index] - t_1[index - 1]) * tarifa[index];
                }
                else {
                    return i * tarifa[index];
                }
            });
            if (rest > 0) {
                t_1.push(rest * tarifa[t_1.length]);
            }
            return Number((t_1.reduce(function (a, b) { return a + b; }, 0)).toFixed(0));
        }
        else {
            return Number((energy * tarifa[0]).toFixed(0));
        }
    };
    ElectricComsumption.prototype.calculateEbikeComsCost = function (hadEbike) {
        if (hadEbike === void 0) { hadEbike = false; }
        var mensualEnergy = this.calculatePb() * this.times;
        if (hadEbike) {
            return Number((this.calculateCost() - this.calculateCost(this.energy - mensualEnergy)).toFixed(0));
        }
        else {
            return Number((this.calculateCost(this.energy + mensualEnergy) - this.calculateCost()).toFixed(0));
        }
    };
    return ElectricComsumption;
}());
exports.ElectricComsumption = ElectricComsumption;
var App = /** @class */ (function () {
    function App() {
        var _this = this;
        this.chartops = {
            type: 'doughnut',
            plugins: [{
                    afterDraw: function (chartInstance, easing, options) { },
                }, {
                    afterDraw: function (chartInstance, easing, options) { },
                }],
            data: {
                labels: ['Vehículo Eléctrico', 'Vivienda'],
                datasets: [{
                        label: 'Precio',
                        backgroundColor: ['rgb(0, 124, 204)', 'rgb(15, 82, 186)'],
                        borderColor: ['rgb(0, 124, 204)', 'rgb(15, 82, 186)']
                    }],
                borderWith: 1
            },
            animationEnabled: true,
            options: {
                maintainAspectRatio: true,
                animation: {
                    duration: 1000,
                    easing: 'easeInOutCirc'
                },
                cutoutPercentage: 60,
                legend: {
                    display: false,
                    labels: {
                        fontColor: 'white',
                    }
                }
            }
        };
        var consumoTotalDinero;
        var consumoTotalkW;
        var consumoVEDinero;
        var consumoVEkW;
        var calcularForm = document.querySelector('#calcularForm');
        var response = document.querySelector('#response');
        var formsValidate = document.querySelector(".needs-validation");
        this.chart = new Chart(document.getElementById("mychart").getContext('2d'), this.chartops);
        var hadEbike = document.querySelector("#checkHadEbike");
        hadEbike.addEventListener('change', function (e) {
            var toast = document.querySelector('.toast-body');
            toast.innerHTML = (hadEbike.checked ? 'Incluido ' : 'Excluido ') + 'consumo del Vehículo Eléctrico en el Consumo Mensual';
            toastError.show();
        });
        var checkTokW = document.querySelector("#checkTokW");
        checkTokW.addEventListener('change', function (e) {
            if (checkTokW.checked) {
                _this.response(consumoVEkW, consumoTotalkW, true);
            }
            else {
                _this.response(consumoVEDinero, consumoTotalDinero, false);
            }
        });
        var btnCalcular = document.querySelector('#btnCalcular');
        btnCalcular.addEventListener('click', function (e) {
            e.preventDefault();
            checkTokW.checked = false;
            var energy = document.querySelector('#inputEnergy');
            var times = document.querySelector("#inputTimes");
            var voltage = document.querySelector("#inputVoltage");
            var current = document.querySelector("#inputCurrent");
            var n = document.querySelector("#inputEfficience");
            var typeVE = document.querySelector("#tipoVE");
            var marcaVE = document.querySelector('#marcaVE');
            var hadEbike = document.querySelector("#checkHadEbike");
            try {
                var calculo = new ElectricComsumption(Number(energy.value), Number(times.value), Number(current.value), Number(n.value), Number(voltage.value));
                consumoTotalkW = hadEbike.checked ? calculo.energy : calculo.energy + calculo.calculatePb() * calculo.times;
                consumoTotalDinero = Number(calculo.calculateCost(Number(consumoTotalkW)));
                consumoVEDinero = calculo.calculateEbikeComsCost(hadEbike.checked);
                consumoVEkW = calculo.calculatePb() * calculo.times;
                formsValidate.classList.add('was-validated');
                try {
                    _this.response(consumoVEDinero, consumoTotalDinero);
                    if (typeVE.value !== "Seleccionar" && marcaVE.value !== "Seleccionar") {
                        typeVE.classList.remove('is-invalid');
                        marcaVE.classList.remove('is-invalid');
                        var datos = new Datos();
                        var user = Parse.User.current();
                        datos.set('userrel', user);
                        datos.set('energia_casa', Number(energy.value));
                        datos.set('tipo_ve', typeVE.value);
                        datos.set('marca_ve', marcaVE.value);
                        datos.set('cant_cargas', Number(times.value));
                        datos.set('bateria_tension', Number(voltage.value));
                        datos.set('bateria_corriente', Number(current.value));
                        datos.save().then(function (result) {
                            calcularForm.classList.replace('fadeIn', 'fadeOut');
                            response.classList.replace('fadeOut', 'fadeIn');
                            setTimeout(function () {
                                _this.chart.render();
                            }, 1000);
                        }).catch(function (err) {
                            var toast = document.querySelector('.toast-body');
                            toast.innerHTML = "No hay conexi\u00F3n " + err.message;
                            toastError.show();
                        });
                    }
                    else if (typeVE.value === 'Seleccionar') {
                        formsValidate.classList.remove('was-validated');
                        typeVE.classList.add('is-invalid');
                        var toast = document.querySelector('.toast-body');
                        toast.innerHTML = 'Seleccione el Tipo de Vehículo Eléctrico';
                        toastError.show();
                    }
                    else if (marcaVE.value === 'Seleccionar') {
                        formsValidate.classList.remove('was-validated');
                        marcaVE.classList.add('is-invalid');
                        var toast = document.querySelector('.toast-body');
                        toast.innerHTML = 'Seleccione la Marca del Vehículo Eléctrico';
                        toastError.show();
                    }
                }
                catch (error) {
                    var toast = document.querySelector('.toast-body');
                    toast.innerHTML = error.message;
                    toastError.show();
                }
            }
            catch (error) {
                var toast = document.querySelector('.toast-body');
                toast.innerHTML = error.message;
                toastError.show();
            }
        });
        var btnReCalcular = document.querySelector('#btnReCalcular');
        btnReCalcular.addEventListener('click', function (e) {
            formsValidate.classList.remove('was-validate');
            calcularForm.classList.replace('fadeOut', 'fadeIn');
            response.classList.replace('fadeIn', 'fadeOut');
        });
    }
    App.prototype.response = function (consumoVE, consumoTotal, checkTokW) {
        if (checkTokW === void 0) { checkTokW = false; }
        if (consumoVE < consumoTotal) {
            var consumoVivienda = consumoTotal - consumoVE;
            this.animateValue('#counter', 0, consumoTotal - consumoTotal % 1, 1000);
            this.animateValue('#counter_Vivienda', 0, consumoVivienda - consumoVivienda % 1, 1000);
            this.animateValue('#counter_EMotoCons', 0, consumoVE - consumoVE % 1, 1000);
            this.chart.destroy();
            this.chart = new Chart(document.getElementById("mychart").getContext('2d'), this.chartops);
            this.chart.data.datasets[0].data = [consumoVE, consumoTotal - consumoVE];
            this.makePercentage(this.chart);
            this.chart.update();
            var unidadDinSpans = document.querySelectorAll(".unidad_dinero");
            var unidadEnSpans = document.querySelectorAll(".unidad_kW");
            unidadDinSpans.forEach(function (val) {
                val.innerHTML = checkTokW ? "" : "$";
            });
            unidadEnSpans.forEach(function (val) {
                val.innerHTML = checkTokW ? "kWh" : "";
            });
        }
        else {
            throw new RangeError("El consumo del vehículo eléctrico excede el consumo total");
        }
    };
    App.prototype.animateValue = function (id, start, end, duration) {
        if (start === end)
            return;
        var range = end - start;
        var current = start;
        var increment = end > start ? 1 : -1;
        var stepTime = Math.abs(Math.floor(duration / range));
        var obj = document.querySelector(id);
        var timer = setInterval(function () {
            current += increment;
            obj.innerHTML = String(current);
            if (current == Number(end.toFixed(0))) {
                clearInterval(timer);
            }
        }, stepTime);
    };
    App.prototype.makePercentage = function (thischart) {
        Chart.pluginService.register({
            beforeDraw: function (thischart) {
                var width = thischart.chart.width, height = thischart.chart.height, ctx = thischart.chart.ctx, type = thischart.config.type;
                if (type == 'doughnut') {
                    var percent = Math.round((thischart.config.data.datasets[0].data[0] * 100) /
                        (thischart.config.data.datasets[0].data[0] +
                            thischart.config.data.datasets[0].data[1]));
                    var oldFill = ctx.fillStyle;
                    var fontSize = ((height - thischart.chartArea.top) / 90).toFixed(2);
                    ctx.restore();
                    ctx.font = fontSize + "em sans-serif";
                    ctx.textBaseline = "middle";
                    var text = percent + "%", textX = Math.round((width - ctx.measureText(text).width) / 2), textY = (height + thischart.chartArea.top) / 2;
                    ctx.fillStyle = thischart.config.data.datasets[0].backgroundColor[0];
                    ctx.fillText(text, textX, textY);
                    ctx.fillStyle = oldFill;
                    ctx.save();
                }
            }
        });
    };
    return App;
}());
exports.App = App;
new App();
// export {ElectricComsumption, App}
//# sourceMappingURL=index.js.map