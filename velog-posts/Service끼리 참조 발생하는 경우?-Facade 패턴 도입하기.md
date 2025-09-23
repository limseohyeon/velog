<h1 id="문제">문제</h1>
<hr />
<h2 id="주문-취소-요구사항에-대한-정리">주문 취소 요구사항에 대한 정리</h2>
<ol>
<li>하나의 아이템에 대한 취소(=주문 상세 취소)<ol>
<li>주문(Order) 의 결제 금액(total_price) : 주문 상세(Order_detail)의 총액(total_price) 만큼 감소</li>
<li>상품(Item)의 재고 : 주문 상세의 주문 수량 만큼 증가</li>
</ol>
</li>
</ol>
<h2 id="고민">고민</h2>
<p><strong>해당 기능 구현 방법</strong></p>
<p>방법1. OrderDetailService에서 Item의 상품 제고 변경 Service와 Order의 총액 변경 Service를 사용하기</p>
<p>방법2. OrderDetailService에서 Item의 Respository와 Order의 Repository를 직접 다루기</p>
<p>두가지 방법 모두 OrderDetailService의 역할이 너무 많은 책임을 가지게 되고(SRP위반), Order, Item, OrderDetail 간의 의존성이 얽히게 된다.</p>
<p>이렇게 되면 서비스 내부에서 순환참조가 발생할 가능성도 있을 뿐더러 유지 보수, 성능 측면에서도 좋은 성능을 내지 못 할 것이라는 생각이 들었다. </p>
<p>또한 직접적으로 Serive를 쓰니 순환참조 문제가 발생했다.</p>
<h1 id="해결---퍼사드-패던-도입하기">해결 - 퍼사드 패던 도입하기</h1>
<hr />
<p>updateOrderDetailCountService 라는 퍼사드를 만들어 퍼사드 내부에서 OrderService, ItemService를 주입 받게 했다.</p>
<p>또한, 사용자 뿐만 아니라<code>관리자</code>가 <strong>주문을 취소하는 경우</strong>에도 동일한 로직이 사용되기 때문에 해당 Service를 재사용할 수 있으면 좋겠다는 생각이 들었다. 이를 위해 domain 에서 분리 시켜 grobal에서 별도의 Service디렉터리를 생성했다. 여기서 주문 취소/변경에 대한 service들을(퍼사드에 주입될 Service) 별도로 관리하고 이를 퍼사드에 주입시켜 사용할 수 있게 변경했다.</p>
<h2 id="구현-코드">구현 코드</h2>
<h3 id="grobal-service">Grobal Service</h3>
<p><strong>UpdateAllStockService.class</strong></p>
<ul>
<li>전체 주문(Order)취소 시 Order의 모든 OrderDetail의 Item별 재고 원복하는 class</li>
</ul>
<pre><code class="language-java">package org.programmer.cafe.service;

import java.util.List;
import lombok.RequiredArgsConstructor;
import org.programmer.cafe.domain.item.entity.Item;
import org.programmer.cafe.domain.item.entity.dto.UpdateItemRequest;
import org.programmer.cafe.domain.item.repository.ItemRepository;
import org.programmer.cafe.domain.order.entity.Order;
import org.programmer.cafe.domain.order.repository.OrderRepository;
import org.programmer.cafe.domain.orderdetail.entity.OrderDetail;
import org.programmer.cafe.domain.orderdetail.repository.OrderDetailRepository;
import org.programmer.cafe.exception.BadRequestException;
import org.programmer.cafe.exception.ErrorCode;
import org.springframework.stereotype.Service;

@RequiredArgsConstructor
@Service
public class UpdateAllStockService {

    private final OrderRepository orderRepository;
    private final OrderDetailRepository orderDetailRepository;
    private final ItemRepository itemRepository;

    public void updateOrderStock(Long orderId){
        Order order = orderRepository.findById(orderId)
            .orElseThrow(() -&gt; new BadRequestException(ErrorCode.NONEXISTENT_ITEM));

        List&lt;OrderDetail&gt; orderDetail = orderDetailRepository.findAllByOrder_Id(orderId);

        for(OrderDetail list : orderDetail){
            Item item = list.getItem();
            int count = list.getCount();    // 주문 수량
            int updatedStock = item.getStock() + count; // 바뀌는 재고

            UpdateItemRequest updateItemRequest = UpdateItemRequest.builder()
                .name(item.getName())
                .image(item.getImage())
                .price(item.getPrice())
                .stock(updatedStock)
                .status(item.getStatus())
                .build();

            item.update(updateItemRequest);
        }
    }
}</code></pre>
<p><strong>UpdateItemStockService.class</strong></p>
<ul>
<li>하나의 주문 상세를 취소하는 경우 주문 수량만큼 Item의 재고를 원복하는 class</li>
</ul>
<pre><code class="language-java">package org.programmer.cafe.service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.programmer.cafe.domain.item.entity.Item;
import org.programmer.cafe.domain.item.entity.dto.UpdateItemRequest;

import org.programmer.cafe.domain.item.repository.ItemRepository;

import org.programmer.cafe.domain.orderdetail.entity.dto.UserOrderDetailRequest;
import org.programmer.cafe.domain.orderdetail.repository.OrderDetailRepository;
import org.programmer.cafe.exception.BadRequestException;
import org.programmer.cafe.exception.ErrorCode;
import org.springframework.stereotype.Service;

@Slf4j
@RequiredArgsConstructor
@Service
public class UpdateItemStockService {

    private final ItemRepository itemRepository;
    private final OrderDetailRepository orderDetailRepository;

    // 주문 수량 변경 서비스
    public UserOrderDetailRequest updateItemStock(Long orderDetailId, int newCount,
        UserOrderDetailRequest userOrderDetailRequest) {

        Item item = itemRepository.findById(userOrderDetailRequest.getItemId())
            .orElseThrow(() -&gt; new BadRequestException(
                ErrorCode.NONEXISTENT_ITEM));
        int updatedStock = item.getStock() + (userOrderDetailRequest.getCount() - newCount);

        //재고 변경
        UpdateItemRequest updateItemRequest = UpdateItemRequest.builder()
            .name(item.getName())
            .image(item.getImage())
            .price(item.getPrice())
            .stock(updatedStock)
            .status(item.getStatus())
            .build();

        // 수량 업데이트
        UserOrderDetailRequest updatedRequest = userOrderDetailRequest.toBuilder()
            .count(newCount)
            .build();

        return userOrderDetailRequest;
    }
}</code></pre>
<p>UpdateOrderDetailPriceService.class</p>
<ul>
<li>주문 상세의 주문 수량을 변경하는 경우 주문 상세 총액을 변경하는 class</li>
</ul>
<pre><code class="language-java">package org.programmer.cafe.service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.programmer.cafe.domain.item.entity.Item;
import org.programmer.cafe.domain.item.repository.ItemRepository;
import org.programmer.cafe.domain.orderdetail.entity.dto.UserOrderDetailRequest;
import org.programmer.cafe.exception.BadRequestException;
import org.programmer.cafe.exception.ErrorCode;
import org.springframework.stereotype.Service;

// 주문 상세 총액 변경
@Slf4j
@RequiredArgsConstructor
@Service
public class UpdateOrderDetailPriceService {

    private final ItemRepository itemRepository;

    public UserOrderDetailRequest updateOrderDetailPriceService(Long orderDetailId, int newCount,
        UserOrderDetailRequest userOrderDetailRequest) {

        Item item = itemRepository.findById(userOrderDetailRequest.getItemId())
            .orElseThrow(() -&gt; new BadRequestException(ErrorCode.NONEXISTENT_ITEM));

        int newTotalPrice = item.getPrice() * newCount;

        UserOrderDetailRequest updatedRequest = userOrderDetailRequest.toBuilder()
            .totalPrice(newTotalPrice).build();

        return updatedRequest;
    }
}</code></pre>
<p><strong>UpdateOrderPriceService.class</strong></p>
<ul>
<li>OrderderDetail의 총액 변경에 따라 주문(Order)의 총액을(결제금액을) 변경하는 class</li>
</ul>
<pre><code class="language-java">package org.programmer.cafe.service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.programmer.cafe.domain.order.entity.Order;
import org.programmer.cafe.domain.order.repository.OrderRepository;
import org.programmer.cafe.domain.orderdetail.entity.dto.UserOrderDetailRequest;
import org.programmer.cafe.exception.BadRequestException;
import org.programmer.cafe.exception.ErrorCode;
import org.springframework.stereotype.Service;

// 주문 금액 변경
@Slf4j
@RequiredArgsConstructor
@Service
public class UpdateOrderPriceService {

    private final OrderRepository orderRepository;

    public void updateOrderPrice(Long orderId, UserOrderDetailRequest userOrderDetailRequest,
        int oldTotalPrice, int oldPayment) {

        int newPayment = (oldPayment - oldTotalPrice) + userOrderDetailRequest.getTotalPrice();

        UserOrderDetailRequest updatedRequest = userOrderDetailRequest.toBuilder()
            .totalPrice(newPayment)
            .build();

        Order order = orderRepository.findById(orderId)
            .orElseThrow(() -&gt; new BadRequestException(ErrorCode.NONEXISTENT_ITEM));

        order.updateTotalPrice(newPayment);

    }
}</code></pre>
<p><strong>UpdateStatusService.class</strong></p>
<ul>
<li>주문 상태를 변경하는 class</li>
</ul>
<pre><code class="language-java">package org.programmer.cafe.service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.programmer.cafe.domain.order.entity.Order;
import org.programmer.cafe.domain.order.entity.OrderStatus;
import org.programmer.cafe.domain.order.repository.OrderRepository;
import org.programmer.cafe.exception.BadRequestException;
import org.programmer.cafe.exception.ErrorCode;
import org.springframework.stereotype.Service;

@Slf4j
@RequiredArgsConstructor
@Service
public class UpdateStatusService {

    private final OrderRepository orderRepository;

    public void updateStatus(Long orderId,
        OrderStatus updateStatus) {
        Order order = orderRepository.findById(orderId)
            .orElseThrow(() -&gt; new BadRequestException(ErrorCode.NONEXISTENT_ITEM));

        OrderStatus newStatus = order.getStatus();

        if (order.getStatus() == OrderStatus.CANCEL) {
            throw new BadRequestException(ErrorCode.ORDER_ALREADY_CANCELED);
        }

        if (order.getStatus() == OrderStatus.SHIPPING_STARTED &amp;&amp; updateStatus == OrderStatus.CANCEL) {
            throw new BadRequestException(ErrorCode.ORDER_ALREADY_STARTED);
        }

        log.info(&quot;Updating status of order {} to {}&quot;, orderId, newStatus);

        switch (updateStatus) {
            case COMPLETED:
            case SHIPPING_STARTED:
            case CANCEL:
                order.updateStatus(updateStatus);
                break;
            default:
                throw new BadRequestException(ErrorCode.BAD_REQUEST);
        }

    }

}</code></pre>
<h3 id="pasade-service">Pasade Service</h3>
<p><strong>UserOrderDetailService.class</strong></p>
<pre><code class="language-java"> @Transactional
    public void updateOrderDetailCountService(Long orderDetailId, int newCount,
        UserOrderDetailRequest userOrderDetailRequest) {

        if (newCount &lt;= 0) {
            throw new BadRequestException(ErrorCode.COUNT_BELOW_MINIMUM);
        }

        Order order = orderRepository.findById(userOrderDetailRequest.getOrderId())
            .orElseThrow(() -&gt; new BadRequestException(ErrorCode.NONEXISTENT_ITEM));

        int oldTotalPrice = userOrderDetailRequest.getTotalPrice();
        int oldPayment = order.getTotalPrice();
        UserOrderDetailRequest updatedRequest = updateItemStockService.updateItemStock(
            orderDetailId, newCount, userOrderDetailRequest);
        updatedRequest = updateOrderDetailPriceService.updateOrderDetailPriceService(orderDetailId,
            newCount, updatedRequest);
        updateOrderPriceService.updateOrderPrice(order.getId(), updatedRequest, oldTotalPrice,
            oldPayment);
        orderDetailRepository.save(OrderDetailMapper.INSTANCE.toEntity(updatedRequest));
    }</code></pre>
<h1 id="결과">결과</h1>
<hr />
<ul>
<li><strong>모듈 분리</strong> : 우선 도메인간 응집도가 낮아졌을 뿐만 아니라 기존 OrderDetail의 너무 많은 역할을 분리 시킬 수 있었다.</li>
<li>테스트 시에서도 각 플로우에 대한 테스트만 진행하면 됐기 때문에 테스트 시간이 단축될 수 있었다.</li>
<li><strong>유지보수 및 변경에 대한 용이성 증가</strong> : 또한, 이후 할인 정책과 같은 복합 조건이 들어가는 경우 등 정책이 변경이 되는 경우에 대해 대비도 가능하게 되었다.</li>
<li>퍼사드는 기능 조합자 역할만 실제 비즈니스 규칙은 Service에 집중해 OCP(Open closed principle) 개방폐쇄원칙도 지킬 수 있게 되었다.</li>
</ul>